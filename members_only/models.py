from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class Photo(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')

# Added by Model 2
class VerificationCharge(models.Model):
    """
    Stores the time and amount of a charge for a User to verify
    """
    timestamp = models.DateTimeField(default=None, null=True)
    amount = models.IntegerField(default=0)


class User(AbstractUser):
    """
    Defines the attributes of a User.
    """

    first_name  = models.CharField(max_length=50,null=True)
    last_name   = models.CharField(max_length=50,null=True)
    invited_by   = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    visibility  = models.BooleanField(default=False, null=True)
    points      = models.IntegerField(default=0)
    user_type   = models.CharField(max_length=50,null=True)
    date_create = models.DateTimeField(auto_now_add = True,null=True)
    is_verified = models.BooleanField(default=True,null=True)
    birthday    = models.CharField(max_length=50,null=True)
    address = models.TextField(default="")
    blocked_members = models.ManyToManyField("self", blank=True, )
    reset_code = models.CharField(max_length=10, default="")

    # Added by Model 2 
    stripe_card = models.CharField(max_length=50)
    stripe_customer = models.CharField(max_length=50)
    verification_charge = models.ForeignKey(VerificationCharge, on_delete=models.CASCADE, default=None, null=True)
    last_verified = models.DateTimeField(default=None, null=True) # Date of last verification (If repeated verification is wanted)


class Post(models.Model):
    """
    Post inherits from a base model.
    """

    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    urls            = models.TextField(null=True)
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    date_modified   = models.DateTimeField(auto_now=True, null=True)
    is_flagged      = models.BooleanField(default=False, null=True)
    content         = models.TextField(max_length=1000000, null=True)
    by_admin        = models.BooleanField(default=False, null=True)

class Comment(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    sponsored_items = models.ForeignKey("self", on_delete=models.CASCADE,null=True)
    content         = models.TextField(max_length=1000000)
    date_created    = models.DateTimeField(auto_now_add=True, null=True)
    date_modified   = models.DateTimeField(auto_now=True, null=True)
    by_admin        = models.BooleanField(default=False, null=True)

class CreditCard(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    card_num        = models.CharField(max_length=16, null=True)
    cvv             = models.CharField(max_length=3, null=True)
    holder_name     = models.CharField(max_length=50, null=True)
    card_expiration = models.CharField(max_length=25, null=True)
    currently_used  = models.BooleanField(default=True, null=True)
    address         = models.CharField(max_length=50,null=True)
    zipcode         = models.IntegerField(null=True)

class ShortLink(models.Model):
    originalURL = models.URLField()
    short_token = models.CharField(max_length=10,null=True)


class Image(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post                = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image_original      = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    filter_used         = models.BooleanField(default=False, null=True)
    current_image       = models.ImageField(null=True)
    is_flagged          = models.BooleanField(default=False, null=True)
    by_admin            = models.BooleanField(default=False, null=True)

class Filter(models.Model):
    image       = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    filter_name = models.CharField(max_length=16, null=True)

    def data(self):
        return self.__dict__

