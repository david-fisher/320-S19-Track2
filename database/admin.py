from django.contrib import admin

from .form import MemberForm
from .models import Member


class StatusAdmin(admin.ModelAdmin):
    list_display = [
                    'ccid',
                    'postid',
                    'visibility',
                    'invitedby',
                    'email',
                    'password',
                    'username',
                    'points',
                    'usertype',
                    'logintime',
                    'logouttime',
                    'isVerified',
                    'birthday',
                    'address'
                    ]
    
    
    form = MemberForm
    class Meta:
        model = Member
        
        
admin.site.register(Member, StatusAdmin)