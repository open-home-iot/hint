from django.db.models.signals import post_delete
from django.contrib.auth import models as auth_models
from django.dispatch import receiver

from backend.hume.models import Hume


@receiver(post_delete, sender=auth_models.User, dispatch_uid='user_deleted')
def on_user_deleted(sender, instance, using, **kwargs):
    """
    This function works for both Users and HUME Users.

    :param sender: the post_delete signal
    :param instance:
    :param using:
    :param kwargs: ignored
    :return: N/A
    """
    print("DELETING!")
    for hume in Hume.objects.filter(users__isnull=True):
        hume.delete()
