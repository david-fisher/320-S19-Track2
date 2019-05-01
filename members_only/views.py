from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from members_only.models import User, Post, Comment, Image, ShortLink
from members_only.serializers import UserSerializer, UserSetupSerializer, PostSerializer, CommentSerializer, ImageSerializer, ShortLinkSerializer
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
                new_user.first_name = serializer.data['first_name']
                new_user.last_name = serializer.data['last_name']
                new_user.address = serializer.data['address']

                new_user.set_password(serializer.data['password'])
                new_user.save()

                Response({"message": "User registered successfully"})
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

    @action(detail=False, methods=['get'], serializer_class=PostSerializer, permission_classes=[])
    def get_post(self, request):
        serializer = PostSerializer(request.data)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.order_by('-date_created')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    @action(detail=False, methods=['get'], serializer_class=CommentSerializer, permission_classes=[])
    def get_post(self, request):
        serializer = CommentSerializer(request.data)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    @action(detail=False, methods=['get'], serializer_class=ImageSerializer, permission_classes=[])
    def get_post(self, request):
        serializer = ImageSerializer(request.data)
        return Response(serializer.data)


@api_view(['GET'])
def link_shortening(request):

    try:
        short_link = None  # todo: find out a way to try and get the long url from request.data (involves parsing)
    except ShortLink.DoesNotExist:
        # todo create the short link from
        pass

    if request.method == 'GET':
        serializer = ShortLinkSerializer(short_link)
        return Response(serializer.data)


# I think we may not need a GET long_url,
# since the only time it would be used is when we redirect


@api_view(['GET'])
def image_filters(request):

    if request.method == 'GET':
        pass


@api_view(['PUT', 'POST'])
def apply_filters(request):

    if request.method == 'PUT':
        pass

    if request.method == 'POST':
        pass


@api_view(['PUT'])
def remove_filters(request):

    if request.method == 'PUT':
        pass


@api_view(['POST'])
def edited_comment(request):

    if request.method == 'POST':
        pass
