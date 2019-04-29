from rest_framework import serializers
from members_only.models import Post, Comment, User, Image, ShortLink, VerificationCharge


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'first_name', 'last_name', 'address', 'blocked_members', 'points', 'birthday', 'is_verified', 'invited_by', 'user_type', 'date_create')


class UserSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'reset_code', 'password', 'first_name', 'last_name', 'address', 'stripe_card')

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'reset_code', 'first_name', 'last_name', 'address', 'stripe_card')


class VerificationChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCharge
        fields = ('amount',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'user', 'content', 'urls', 'date_created', 'date_modified', 'is_flagged', 'by_admin')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'url', 'user', 'post', 'content', 'date_created', 'date_modified', 'by_admin')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'url', 'post', 'image_original', 'filter_used', 'current_image', 'is_flagged', 'by_admin')


class ShortLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = ('id', 'originalURL', 'short_token')
