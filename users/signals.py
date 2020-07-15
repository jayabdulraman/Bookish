from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()


def logged_in_message(sender, user, request, **kwargs):
	messages.info(request, f'Welcome {user}!')

user_logged_in.connect(logged_in_message)
