from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import models as auth_models

from hume.models import Hume


@receiver(post_delete, sender=auth_models.User, dispatch_uid='user_deleted')
def on_user_deleted(sender, instance, **kwargs):
    """
    This function works for both Users and HUME Users.

    :param sender: the post_delete signal
    :param instance: the User being deleted
    :param kwargs: ignored
    :return: N/A
    """
    for hume in Hume.objects.filter(users__isnull=True):
        hume.delete()
