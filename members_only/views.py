from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from members_only.models import User, Post, Comment, Image, ShortLink, VerificationCharge
from members_only.serializers import UserSerializer, UserSetupSerializer, PostSerializer, CommentSerializer, ImageSerializer, ShortLinkSerializer, VerificationChargeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from members_only.payment_processing.payment_processing import PaymentProcessor, PaymentProcessorType, APIConnectionError, InvalidAPIKeyError, InvalidRequestError, CardDeclinedError, PaymentAdaptorError, UserNotSetupError, UserAlreadySetupError, NoVerificationChargeError

import members_only.settings as settings

from django.utils import translation  # might not need
import traceback

# Create your views here.


# Front End Views
def index(request):
    return render(request, "index.html")


def homefeed(request):
    return render(request, "HomeFeed.html")


# Back End Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def create(self, request):
        if request.user.points < settings.POINT_COST_FOR_INVITE:
            return Response({"success":False})

        request.user.points -= settings.POINT_COST_FOR_INVITE
        request.user.save()

        response = super().create(request)

        return Response({"success":True})

    @action(detail=False, methods=['post'], serializer_class=UserSetupSerializer, permission_classes=[])
    def setup(self, request):
        serializer = UserSetupSerializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(username=serializer.data['email']).exists():
                new_user = User.objects.get(username=serializer.data['email'])

                if new_user.reset_code != serializer.data['reset_code'] or new_user.reset_code == "":
                    return Response({"message": "Incorrect reset code"})

                new_user.reset_code = ""
                new_user.first_name = serializer.data['first_name']
                new_user.last_name = serializer.data['last_name']
                new_user.address = serializer.data['address']
                
                paymentResponse = setupPayments(new_user, serializer)

                # If payment has failed, don't save the new user, return error message
                if paymentResponse.data['success'] is False:
                    return paymentResponse

                new_user.set_password(serializer.data['password'])
                new_user.save()

                return Response({"message": "User registered successfully"})
            else:
                return Response({"message": "User does not exist"})

        else:
            return Response({"message": "Invalid data"})

    """ ADDED FOR TESTING PURPOSES, SHOULD BE CHECKED BY TORCH JUGGLERS """
    @action(detail=False, methods=['put'], serializer_class=VerificationChargeSerializer, permission_classes=[])
    def verify(self, request):
        serializer = VerificationChargeSerializer(data=request.data)
        if serializer.is_valid():

            """ TODO
                Formalize reponces.
                More detailed resposes from payment processor exceptions
            """

            user = request.user

            if user.is_verified:
                return Response(
                    {
                        "success": True,
                        "message": "User already verified"
                    }
                )

            response = verifyUser(user, serializer)

            if response.data['success'] is False:
                return response
            else:
                user.save()
                return response

        else:
            return Response(
                {
                    "success": False,
                    "message": "Invalid data"
                })

    @action(detail=False, methods=['get'], serializer_class=UserSerializer, permission_classes=[IsAuthenticated])
    def current_user(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by('-date_created')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def create(self, request):

        response = super().create(request)

        request.user.points += settings.POINTS_PER_POST

        request.user.save()

        return response


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('-date_created')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def create(self, request):
        response = super().create(request)

        request.user.points += settings.POINTS_PER_COMMENT

        request.user.save()

        return response


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class ShortLinkViewSet(viewsets.ModelViewSet):
    queryset = ShortLink.objects.all()
    serializer_class = ShortLinkSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


def setupPayments(new_user, serializer):
    try:

        stripe_card = serializer.data['stripe_card']

        pp = PaymentProcessor.create_payment_processor(
            PaymentProcessorType.STRIPE, settings.STRIPE_KEY, new_user)

        # Creates a Stripe Customer token from the given stripe card
        pp.setup_user(stripe_card)

        charge_data = pp.charge()

        new_user.verification_charge = VerificationCharge.objects.create(
            timestamp=charge_data["timestamp"], amount=charge_data["amount"])

        new_user.is_verified = False

        # This print is for testing verification without logging onto stripe interface
        print("Amount charged to user: ", charge_data["amount"])

        return Response({
                        "success": True,
                        "message": "Charge successful",
                        "timestamp": charge_data["timestamp"]
                        })

    except CardDeclinedError:
        return Response(
            {
                "success": False,
                "message": "The credit card was declined."
            }
        )

    except APIConnectionError:
        traceback.print_exc()
        return Response(
            {
                "success": False,
                "message": "Failed to connect to Stripe. Try again soon."
            }
        )

    except (InvalidAPIKeyError, InvalidRequestError, PaymentAdaptorError, UserNotSetupError, UserAlreadySetupError):
        traceback.print_exc()
        return Response(
            {
                "success": False,
                "message": "The server as encountered an error."
            }
        )

    else:
        return Response({"message": "User does not exist"})

def verifyUser(user, serializer):
    try:
        pp = PaymentProcessor.create_payment_processor(
            PaymentProcessorType.STRIPE, settings.STRIPE_KEY, user)

        amount = serializer.data['amount']

        if pp.verify(amount):
            return Response(
                {
                    "success": True,
                    "message": "User is verified"
                }
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Incorrect amount."
                })

    except NoVerificationChargeError:
        return Response(
            {
                "success": False,
                "message": "No verification charge is on the account."
            })

    except PaymentAdaptorError:
        traceback.print_exc()
        return Response(
            {
                "success": False,
                "message": "The server has encountered an exception."
            })