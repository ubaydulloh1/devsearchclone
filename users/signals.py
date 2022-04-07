from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings



# @receiver(post_save, sender=Profile)
def profileCreate(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.first_name,
            username=user.username,
            email=user.email,
        )

        subject = "Welcome To DevSearch Platform!"
        message_body = "We are glad of you joined)."

        send_mail(
            subject,
            message_body,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateAccount(sender, instance, created, **kwargs):
    
    if created == False:
        profile = instance
        user = profile.user
        
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def userDelete(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    print("User Deleting...")

post_save.connect(profileCreate, sender=User)
post_save.connect(updateAccount, sender=Profile)
post_delete.connect(userDelete, sender=Profile)
