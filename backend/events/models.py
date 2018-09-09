from django.db import models

from device.models import Device


# Create your models here.
class Log(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=False)

    timestamp = models.DateTimeField(editable=False, auto_now_add=True)

    type = models.IntegerField(editable=False)
    value = models.IntegerField(editable=False)
