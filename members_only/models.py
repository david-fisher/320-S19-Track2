from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image
from PIL import ImageFilter

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
    stripe_customer = models.CharField(max_length=100, default="")
    last_verified = models.DateTimeField(default=None, null=True)
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

class sponsoredImageInsertion:

    def insert(mg, sponsored_item):
        # retrieve the width and height of the image for the scale
        width, height = img.size

        # create a scale for insert to be resized to
        width_scale = round(width/4)
        height_scale = round(height/4)
        print(width_scale)
        print(height_scale)

        # create a copy of the original image
        img_copy = img.copy()

        # retrieve the proper sponsored item insert
        insert = Image.open('sponsored_items/' + sponsored_item + '.jpg')

        # resize the sponsored item
        insert = insert.resize((width_scale,height_scale))

        for x in range(width_scale):
            for y in range(height_scale):
                pixel = insert.getpixel((x, y))
                img_copy.putpixel((x, y), pixel)

        # return the image with the sponsored content inserted
        return img_copy

class ClubFilter:

    # Class' attributes
    filter_name = "club_filter"
    filter_preview_url = ""

    # Filter method
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((x,y))
                # Remove the Green values from that pixel and apply the change to the image
                img_copy.putpixel((x,y), (r, 0, b))

        return img_copy


class Grayscale:

    # Class attributes
    filter_name = "grayscale"
    filter_preview_url = ""

    # Filter method
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((x, y))
                average = round(((r + b + g)/3))
                # Change the RGB values to make the photo gray
                img_copy.putpixel((x, y), (average, average, average))

        return img_copy


class Negative:

    # Class' attributes
    filter_name = "negative"
    filter_preview_url = ""

    # Filter method
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((x,y))
                # Subtract the r g b values from 255 in order to get the inverted values
                img_copy.putpixel((x,y), (255-r, 255-g, 255-b))

        return img_copy

class Sepia:

    # Class' attributes
    filter_name = "sepia"
    filter_preview_url = ""

    # Filter method
    def filter(img):
        # Retrieve the width and height of the image
        width, height = img.size

        # Create a copy of the original image
        img_copy = img.copy()

        # Two for loops in order to change each pixel
        for x in range(width):
            for y in range(height):
                # Take the pixel at (x, y)
                r, g, b = img.getpixel((x,y))
                # Subtract the r g b values from 255 in order to get the inverted values
                sepiaR = (r * 0.393 + g * 0.769 + b * 0.189)
                sepiaG = (r * 0.349 + g * 0.686 + b * 0.168)
                sepiaB = (r * 0.272 + g * 0.534 + b * 0.131)
                if sepiaR > 255:
                    sepiaR = 255
                if sepiaG > 255:
                    sepiaG = 255
                if sepiaB > 255:
                    sepiaB = 255
                img_copy.putpixel((x,y), (int(sepiaR), int(sepiaG), int(sepiaB)))

        return img_copy
