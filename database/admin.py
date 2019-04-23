from django.contrib import admin
from .models import Member, Post, Comment, CreditCard, Filter, Image

# Register your models here.
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CreditCard)
admin.site.register(Filter)
admin.site.register(Image)
