import logging
from django.db import DatabaseError
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except DatabaseError:
            logger.exception("Failed to create profile for user %s", instance.pk)
            return

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        profile, _ = Profile.objects.get_or_create(user=instance)
    except DatabaseError:
        return
    profile.save()
