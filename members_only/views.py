from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from members_only.models import User, Post, Comment, Image, ShortLink, VerificationCharge
from members_only.serializers import UserSerializer, UserSetupSerializer, PostSerializer, CommentSerializer, ImageSerializer, ShortLinkSerializer
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


def feed(request):
    return render(request, "feed.html")


# Back End Views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

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
                    print( paymentResponse.data['message'] )
                    return paymentResponse

                new_user.set_password(serializer.data['password'])
                new_user.save()

                return Response({"message": "User registered successfully"})
            else:
                return Response({"message": "User does not exist"})

        else:
            return Response({"message": "Invalid data"})

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

        return_val = super().create(request)

        request.user.points += settings.POINTS_PER_POST

        request.user.save()

        return return_val


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('-date_created')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def create(self, request):
        return_val = super().create(request)

        request.user.points += settings.POINTS_PER_COMMENT

        request.user.save()

        return return_val


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
    # TODO: This could be extracted into another function
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
