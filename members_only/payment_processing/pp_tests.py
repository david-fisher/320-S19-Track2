import unittest
import stripe
from pp_tests_user import User
from payment_processing import PaymentProcessor, PaymentProcessorType, StripeAdapter
import payment_processing as PP
import datetime as dt


class PaymentProcessingUnitTest(unittest.TestCase):

    def setUp(self):
        self.APIKey = "sk_test_olr9DVGJZ9ckaU3y2dkqtDja"

        self.TestUser = User("Test", "User", None)

        pp = PaymentProcessor.factory(
            PaymentProcessorType.STRIPE, self.APIKey, self.TestUser)

        pp.setup_user("tok_visa")

    def test_factory_returns_correct_adaptor(self):
        pp = PaymentProcessor.factory(
            PaymentProcessorType.STRIPE, self.APIKey, None)

        self.assertIsInstance(pp, StripeAdapter)

    def test_factory_returns_incorrect_adaptor_error(self):
        with self.assertRaises(PP.PaymentAdaptorError):
            PaymentProcessor.factory(-1, self.APIKey, None)

    def test_setupUser_returns_valid_token(self):

        try:
            user = User("FirstName", "LastName", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.setup_user("tok_visa")
        except Exception:
            self.assertTrue(False)

        self.assertTrue(True)

    def test_setupUser_rejects_invalid_token(self):

        with self.assertRaises(PP.InvalidRequestError):
            user = User("FirstName", "LastName", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.setup_user("tok_wrong")

    def test_setupUser_card_declined(self):

        with self.assertRaises(PP.CardDeclinedError):
            user = User("FirstName", "LastName", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.setup_user("tok_chargeDeclined")

    def test_setupUser_exception_on_already_setup_user(self):

        with self.assertRaises(PP.UserAlreadySetupError):
            user = User("FirstName", "LastName", "cus_token")

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.setup_user("tok_visa")

    def test_charge_succeeds(self):
        try:
            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                self.TestUser
            )

            pp.charge()

            self.assertTrue(True)

        except Exception:
            self.assertTrue(False)

    def test_charge_declined(self):
        with self.assertRaises(PP.CardDeclinedError):
            user = User("Decline", "Charge", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.setup_user("tok_chargeCustomerFail")

            pp.charge()

    def test_charge_user_not_setup(self):
        with self.assertRaises(PP.UserNotSetupError):
            user = User("Decline", "Charge", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.charge()

    def test_charge_user_needs_verification(self):

        user = User("Needs", "Verification", None)

        user.is_verified = True
        user.last_verified = dt.datetime.now() - dt.timedelta(days=91)

        pp = PaymentProcessor.factory(
            PaymentProcessorType.STRIPE,
            self.APIKey,
            user
        )

        pp.setup_user("tok_visa")

        pp.charge()

        self.assertFalse(user.is_verified)

    def test_charge_user_does_not_need_verification(self):
        user = User("NotNeed", "Verification", None)

        user.is_verified = True
        user.last_verified = dt.datetime.now() - dt.timedelta(days=20)

        pp = PaymentProcessor.factory(
            PaymentProcessorType.STRIPE,
            self.APIKey,
            user
        )

        pp.setup_user("tok_visa")

        pp.charge()

        self.assertTrue(user.is_verified)

    def test_update_payment_method_success(self):

        try:
            user = User("Decline", "Charge", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                self.TestUser
            )

            pp.update_payment_method("tok_mastercard")

            pp.charge()

            self.assertTrue(True)

        except Exception:
            self.assertTrue(False)

    def test_update_payment_method_declined(self):
        with self.assertRaises(PP.CardDeclinedError):
            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                self.TestUser
            )

            pp.update_payment_method("tok_chargeDeclined")

    def test_update_payment_method_invalid_token(self):
        with self.assertRaises(PP.InvalidRequestError):

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                self.TestUser
            )

            pp.update_payment_method("tok_Invalid")

    def test_update_payment_method_user_not_setup(self):
        with self.assertRaises(PP.UserNotSetupError):
            user = User("Decline", "Card", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.update_payment_method("tok_visa")

    def test_generate_verification_charge_success(self):

        try:
            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                self.TestUser
            )

            pp.charge()

            verif = pp.generate_verification_charge(10)

            self.assertGreater(verif[0], 0)
            self.assertGreater(verif[1], 0)

        except Exception:
            self.assertTrue(False)

    def test_generate_verification_charge_no_charge_found(self):

        with self.assertRaises(PP.NoVerificationChargeError):
            user = User("No", "Charge", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.setup_user("tok_visa")

            pp.generate_verification_charge(10)

    def test_generate_verification_negative_max_days_old(self):
        with self.assertRaises(PP.NoVerificationChargeError):
            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                self.TestUser
            )

            pp.generate_verification_charge(-1)

    def test_generate_verification_user_not_setup(self):

        with self.assertRaises(PP.UserNotSetupError):
            user = User("No", "Charge", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.generate_verification_charge(10)

    def test_verify_success(self):

        self.TestUser.is_verified = False
        self.TestUser.last_verified = dt.datetime.now() - dt.timedelta(days=120)

        pp = PaymentProcessor.factory(
            PaymentProcessorType.STRIPE,
            self.APIKey,
            self.TestUser
        )

        pp.charge()

        charge = pp.generate_verification_charge(10)

        self.assertTrue(pp.verify(charge[1]))
        self.assertTrue(self.TestUser.is_verified)
        self.assertTrue(self.TestUser.verification_charge is None)
        self.assertLess(dt.datetime.now() - self.TestUser.last_verified,
                        dt.timedelta(days=1))

    def test_verify_failure(self):

        self.TestUser.is_verified = False
        self.TestUser.last_verified = dt.datetime.now() - dt.timedelta(days=120)

        last_verified_copy = self.TestUser.last_verified

        pp = PaymentProcessor.factory(
            PaymentProcessorType.STRIPE,
            self.APIKey,
            self.TestUser
        )

        self.TestUser.is_verified = False

        pp.charge()

        pp.generate_verification_charge(10)

        self.assertFalse(pp.verify(-1))
        self.assertFalse(self.TestUser.is_verified)
        self.assertTrue(self.TestUser.verification_charge is not None)
        self.assertTrue(self.TestUser.last_verified is last_verified_copy)

    def test_verify_no_verification_charge(self):

        with self.assertRaises(PP.NoVerificationChargeError):
            user = User("No", "Verif", None)

            pp = PaymentProcessor.factory(
                PaymentProcessorType.STRIPE,
                self.APIKey,
                user
            )

            pp.setup_user("tok_visa")

            pp.generate_verification_charge(10)


unittest.main()