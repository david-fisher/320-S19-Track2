from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Member(models.Model):
    # FK
    visibility = models.BooleanField(default=False, null=True)
    invited_by = models.IntegerField(null=True)

    # ATTRIBUTES 
    email = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50,null=True)
    points = models.IntegerField(null=True)
    user_type = models.CharField(max_length=50,null=True)
    login_time = models.CharField(max_length=50,null=True)
    logout_time = models.CharField(max_length=50,null=True)
    created_date = models.DateTimeField(auto_now_add = True,null=True)
    is_verified = models.BooleanField(default=True,null=True)
    birthday = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.username

    def set_username(self,username): 
        self.username = username
 
    def get_username(self):     
        return self.username

    # We are going to make getters and setters for entire attributes in the future


class Post(models.Model):
    post_id = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    comment_id = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    image_id = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    urls = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now_add=True, null=True)
    is_flagged = models.BooleanField(default=False, null=True)
    content = models.TextField(max_length=1000000, null=True)
    by_admin = models.BooleanField(default=False, null=True)


class Comment(models.Model):
    replies = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=1000000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now_add=True, null=True)
    by_admin = models.BooleanField(default=False, null=True)


class CreditCard(models.Model):
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    card_num = models.CharField(max_length=16, null=True)
    cvv = models.CharField(max_length=3, null=True)
    holder_name = models.CharField(max_length=50, null=True)
    card_expiration = models.CharField(max_length=25, null=True)
    currently_used = models.BooleanField(default=True, null=True)


class Filter(models.Model):
    filter_id = models.IntegerField(null=True)


class Image(models.Model):
    filter_used = models.BooleanField(default=False, null=True)
    original_image = models.ImageField(null=True)
    filtered_versions = ArrayField(models.ImageField(null=True), blank=True, null=True)
    filters_used = ArrayField(models.IntegerField(null=True), blank=True, null=True)
    is_flagged = models.BooleanField(default=False, null=True)
    user_id = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    by_admin = models.BooleanField(default=False, null=True)
