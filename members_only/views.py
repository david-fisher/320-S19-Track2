from django.shortcuts import render
from rest_framework import viewsets
from members_only.models import User, Post, Comment, Photo, ShortLink
from members_only.serializers import UserSerializer, PostSerializer, CommentSerializer, PhotoSerializer, ShortLinkSerializer

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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    serializer_class = CommentSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class ShortLinkViewSet(viewsets.ModelViewSet):
    queryset = ShortLink.objects.all()
    serializer_class = ShortLinkSerializer
