from django.dispatch import receiver
from django.db.models.signals import post_delete
from backend.device.models import Device

from backend.broker import producer


@receiver(post_delete, sender=Device)
def on_delete(instance: Device, **kwargs):
    """
    Send a detach command each time a device is deleted.
    """
    producer.detach(str(instance.hume.uuid), str(instance.uuid))
