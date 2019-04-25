from rest_framework import serializers
from members_only.models import Post, Comment, User, Photo, ShortLink


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'first_name', 'last_name', 'address', 'blocked_members', 'points_balance', 'stripe_card')


class UserSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'reset_code', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'reset_code', 'first_name', 'last_name', 'address', 'stripe_card')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'owner', 'body', 'timestamp', 'photo')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'url', 'owner', 'parent_post', 'body', 'timestamp')


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'url', 'file')


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = ('id', 'originalURL', 'short_token')
