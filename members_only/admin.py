from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from members_only.models import User, Post, Comment, Image, ShortLink, CreditCard, Filter, VerificationCharge

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(VerificationCharge)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CreditCard)
admin.site.register(Filter)
admin.site.register(Image)
admin.site.register(ShortLink)
