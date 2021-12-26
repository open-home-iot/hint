from django.dispatch import receiver
from django.db.models.signals import post_delete
from backend.hume.models import Hume
from backend.user.models import User


@receiver(post_delete, sender=Hume)
def on_delete(instance, **kwargs):
    """
    Delete a deleted Hume's user instance. Cannot be done with cascade as that
    would require reversing the relation between the Hume and User models.
    """
    hume_user = User.objects.get(id=instance.hume_user.id)
    hume_user.delete()
