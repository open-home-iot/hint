from django.db import models

from device.models import Device


# Create your models here.
class Log(models.Model):
    device = models.OneToOneField(Device, on_delete=models.SET_NULL, primary_key=False)

    timestamp = models.DateTimeField(editable=False, auto_now_add=True, null=False, blank=False)

    type = models.IntegerField(editable=False, null=False, blank=False)
    value = models.IntegerField(editable=False, null=False, blank=False)
