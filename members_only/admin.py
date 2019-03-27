from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from members_only.models import User, Post, Comment, Photo, ShortLink

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(ShortLink)

