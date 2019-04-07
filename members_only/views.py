from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from members_only.models import User, Post, Comment, Photo, ShortLink
from members_only.serializers import UserSerializer, UserSetupSerializer, PostSerializer, CommentSerializer, PhotoSerializer, ShortLinkSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


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
