from members_only.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import random, string

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        reset_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        send_mail(
            "You've been invited to MembersOnly",
            """
            Hello, 
            
            You've been invited to MembersOnly. 
            
            Follow this link to finish setup at https://members-only.com/user/setup and use {} as your access code. 
            
            Thanks, Staff""".format(reset_code),
            "admin@membersonly.com",
            [instance.email],
            fail_silently=True,
        )

        instance.reset_code = reset_code
        instance.save()
