from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
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
