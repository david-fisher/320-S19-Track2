from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from members_only.models import User, Post, Comment, Photo, ShortLink, VerificationCharge
from members_only.serializers import UserSerializer, UserSetupSerializer, UserRegisterSerializer, PostSerializer, CommentSerializer, PhotoSerializer, ShortLinkSerializer, UserVerificationSerializer, VerificationChargeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from members_only.payment_processing.payment_processing import PaymentProcessor, PaymentProcessorType
from members_only.settings import STRIPE_KEY, POINTS_PER_POST, POINTS_PER_COMMENT
from django.utils import translation # might not need
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
                new_user.set_password(serializer.data['password'])
                new_user.save()
            else:
                return Response({"message": "User does not exist"})

        else:
            return Response({"message": "Invalid data"})
    

    """ ADDED FOR TESTING PURPOSES, SHOULD BE CHECKED BY TORCH JUGGLERS """
    @action(detail=False, methods=['put'], serializer_class=UserRegisterSerializer, permission_classes=[])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            
            """ TODO
                Verify/Update/Save other fields
                Check if reset code is right.
                Formalize reponces.
                More detailed resposes from payment processor exceptions
            """

            if User.objects.filter(username=serializer.data['email']).exists():
                new_user = User.objects.get(username=serializer.data['email'])

                try:
                    pp = PaymentProcessor.factory(PaymentProcessorType.STRIPE, STRIPE_KEY, new_user)

                    pp.setup_user( serializer.data['stripe_card'] )

                    charge_data = pp.charge()

                    new_user.verification_charge = VerificationCharge.objects.create( timestamp=charge_data[0], amount=charge_data[1])

                    new_user.is_verified = False

                    new_user.save()

                    return Response({
                        "timestamp": charge_data[0],
                        "amount": charge_data[1]
                    })

                except Exception as e:
                    traceback.print_exc()
                    return Response({"message": "Failed to charge user"})

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
        
            if user.is_verified :
                return Response({"message": "Already Verified"})

            try:
                pp = PaymentProcessor.factory(PaymentProcessorType.STRIPE, STRIPE_KEY, user)

                if pp.verify( int(request.data['amount']) ) :
                    user.save()
                    return Response({"message": "Verified"})

                else:
                    user.save()
                    return Response({"message": "Incorrect amount"})

                    

            except Exception as e:
                traceback.print_exc()
                return Response({"message": "Failed to verify user. A server exception as occured."})



        else:
            return Response({"message": "Invalid data"})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def create(self, request):

        return_val =  super().create(request)

        request.user.points_balance += POINTS_PER_POST

        request.user.save()

        return return_val
        


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def create(self, request):
        return_val =  super().create(request)

        request.user.points_balance += POINTS_PER_COMMENT

        request.user.save()

        return return_val

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class ShortLinkViewSet(viewsets.ModelViewSet):
    queryset = ShortLink.objects.all()
    serializer_class = ShortLinkSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
