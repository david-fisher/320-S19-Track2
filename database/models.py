from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Member(models.Model):
    # FK
    visibility = models.BooleanField(default=False, null=True)
    invitedby = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    # ATTRIBUTES 
    email = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50,null=True)
    points = models.IntegerField(null=True)
    user_type = models.CharField(max_length=50,null=True)
    date_create = models.DateTimeField(auto_now_add = True,null=True)
    is_verified = models.BooleanField(default=True,null=True)
    birthday = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=50,null=True)

    def data(self):
        return self.__dict__
        
    def set_visibility(self,visibility): 
        self.visibility = visibility

    def set_email(self,email): 
        self.email = email
    
    def set_password(self,password): 
        self.password = password

    def set_username(self,username): 
        self.username = username
    
    def set_points(self,points): 
        self.points = points

    def set_user_type(self,user_type): 
        self.user_type = user_type
    
    def set_is_verified(self,is_verified): 
        self.is_verified = is_verified
    
    def set_username(self,username): 
        self.username = username
    
    def set_birthday(self,birthday): 
        self.birthday = birthday
    
    def set_address(self,address): 
        self.address = address
