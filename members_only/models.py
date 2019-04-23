from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class Photo(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')


class User(AbstractUser):
    """
    Defines the attributes of a User.
    """

    # ManyToManyField models an array in this case. Many users could block many Members could block the same Members.
    # Because the ManyToManyField refers to a Member blocking Members, we use "self".
    blocked_members = models.ManyToManyField("self", blank=True, )

    address = models.TextField(default="")
    points_balance = models.IntegerField(default=0)
    stripe_card = models.CharField(max_length=100, default="")
    reset_code = models.CharField(max_length=10, default="")


class Post(models.Model):
    """
    Post inherits from a base model.
    """

    # When the User owning the post is deleted (on_delete), we want to delete all posts associated with that User.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class ShortLink(models.Model):
    originalURL = models.URLField()
    short_token = models.CharField(max_length=10)

