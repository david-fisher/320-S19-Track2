import stripe
import random
import datetime as datetime
from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps

import traceback

# Enum of of implemented payment processor types which can be instantiated


class PaymentProcessorType(Enum):
    STRIPE = 1


class PaymentProcessor(ABC):

    @staticmethod
    def factory(paymentProcessorType, apiKey, user):
        if(paymentProcessorType == PaymentProcessorType.STRIPE):
            return StripeAdapter(apiKey, user)

        raise PaymentAdaptorError("Invalid Payment Processor Type")

    @abstractmethod
    def __init__(self, api_key, user):
        self._api_key = api_key
        self._user = user

    @abstractmethod
    def setup_user(self, token):
        pass

    @abstractmethod
    def charge(self):
        pass

    @abstractmethod
    def update_payment_method(self, token):
        pass

    @abstractmethod
    def generate_verification_charge(self, maxDaysOld):
        pass

    @abstractmethod
    def verify(self, amount):
        pass


class StripeAdapter(PaymentProcessor):

    def __init__(self, api_key, user):
        stripe.api_key = api_key
        super().__init__(api_key, user)

    # Used to wrap Stripe request functions in error handling code
    def _handleStripeError(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except stripe.error.CardError:
                # Payment method declined
                raise CardDeclinedError("Payment method has been declined")
            except stripe.error.RateLimitError:
                # Too many requests made to the API too quickly
                raise APIConnectionError(
                    "Failed to connect to Stripe API - Rate Limit Exceeded")
            except stripe.error.InvalidRequestError:
                # Invalid parameters were supplied to Stripe's API
                raise InvalidRequestError(
                    "Invalid request sent to Stripe - Most likely a sent token was invalid")
            except stripe.error.AuthenticationError:
                # API Key incorrect
                raise InvalidAPIKeyError("Supplied API key is invalid")
            except stripe.error.APIConnectionError:
                # Failed to connect to Stripe
                raise APIConnectionError("Failed to connect to Stripe API")
            except stripe.error.StripeError:
                # Stripe has encountered an error
                raise APIConnectionError("Stripe has encountered and error")
            except UserNotSetupError as e:
                raise e
            except UserAlreadySetupError as e:
                raise e
            except NoVerificationChargeError as e:
                raise e
            except Exception:
                traceback.print_exc()
                # Another error has occurred
                raise PaymentAdaptorError(
                    "The payment adapter has encountered another error")

        return decorated

    @_handleStripeError
    def setup_user(self, token):

        # Check if the user has a customer token
        if self._user.stripe_customer != "":
            raise UserAlreadySetupError(
                "Cannot setup a user who has already been setup")

        # Initialize user as stripe customer object
        responce = stripe.Customer.create(
            description=self._user.first_name + " " + self._user.last_name,
            source=token
        )

        # Get customer token from responce
        self._user.stripe_customer = responce.id

        self._user.is_verified = False
        self._user.verification_charge = None
        self._user.last_verified = None

    @_handleStripeError
    def charge(self):
        if self._user.stripe_customer == None:
            raise UserNotSetupError(
                "The users customer object has not been setup yet")

        amt = random.randint(50, 80)

        resp = stripe.Charge.create(
            amount=amt,
            currency="usd",
            customer=self._user.stripe_customer,
            description="Charge for " + self._user.first_name + " " + self._user.last_name
        )

        if(self._user.last_verified is None or datetime.datetime.now() - self._user.last_verified > datetime.timedelta(days=90)):
            self._user.verified = False

        return (  datetime.datetime.fromtimestamp(resp["created"]), resp["amount"])

    @_handleStripeError
    def update_payment_method(self, token):
        if self._user.stripe_customer == None or self._user.stripe_customer == "":
            raise UserNotSetupError(
                "Cannot change payment method for uninitialized user")

        stripe.Customer.modify(
            self._user.stripe_customer,
            source=token
        )

        return True

    @_handleStripeError
    def generate_verification_charge(self, maxDaysOld):
        if self._user.stripe_customer == None or self._user.stripe_customer == "":
            raise UserNotSetupError(
                "Cannot generate verification charge for uninitialized user")
        
        
        charges = stripe.Charge.list(
            limit=maxDaysOld // 2,
            customer=self._user.stripe_customer,
        )

        validCharges = []

        startDate = datetime.datetime.now() - datetime.timedelta(days=maxDaysOld)

        for charge in charges:
            timestamp = charge["created"]

            date = datetime.datetime.fromtimestamp(timestamp)

            if(date > startDate):
                validCharges.append(charge)

        if(len(validCharges) <= 0):
            raise NoVerificationChargeError(
                "No charges are within the given timespan")

        random.shuffle(validCharges)

        self._user.verification_charge = (
            validCharges[0]["created"], validCharges[0]["amount"])

        return self._user.verification_charge

    def verify(self, amount):
        if self._user.verification_charge == None:
            raise NoVerificationChargeError(
                "No verification charge has been generated for the User")

        print(amount)
        print(self._user.verification_charge.amount)

        if amount == self._user.verification_charge.amount:
            self._user.is_verified = True
            self._user.verification_charge = None
            self._user.last_verified = datetime.datetime.now()
            return True
        else:
            return False


# Errors thrown by

# The API used by the payment processor has failed to connect
class APIConnectionError(Exception):
    pass


# The supplied API Key is invalid
class InvalidAPIKeyError(Exception):
    pass


# Data sent in a request was invalid
class InvalidRequestError(Exception):
    pass


# The payment processor has declined the card on the account
class CardDeclinedError(Exception):
    pass


# The Payment Adaptor has caused an error
class PaymentAdaptorError(Exception):
    pass


# Tried to do an action on a user who has not been setup
class UserNotSetupError(Exception):
    pass


# Tried to do a first time set up on a already setup user
class UserAlreadySetupError(Exception):
    pass


# Tried to do a first time set up on a already setup user
class NoVerificationChargeError(Exception):
    pass
