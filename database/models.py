from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Member(models.Model):
    ## FK
    ccid        = ArrayField(models.IntegerField(null=True), blank=True,null=True)
    postid      = ArrayField(models.IntegerField(null=True), blank=True,null=True)
    visibility  = ArrayField(models.IntegerField(null=True), blank=True,null=True)
    invitedby   = ArrayField(models.IntegerField(null=True), blank=True,null=True)

    # ATTRIBUTES 
    email       = models.CharField(max_length=50,null=True)
    password    = models.CharField(max_length=50,null=True)
    username    = models.CharField(max_length=50,null=True)
    points      = models.IntegerField(null=True)
    usertype    = models.CharField(max_length=50,null=True)
    logintime   = models.CharField(max_length=50,null=True)
    logouttime  = models.CharField(max_length=50,null=True)
    createdData = models.DateTimeField(auto_now_add = True,null=True)
    isVerified  = models.BooleanField(default=True,null=True)
    birthday    = models.CharField(max_length=50,null=True)
    address     = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.username

    def set_username(self,username): 
        self.username = username
 
    def get_username(self):     
        return self.username

    # We are going to make getters and setters for entire attributes in the future