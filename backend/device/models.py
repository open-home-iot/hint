#from django.db import models

#from django.contrib.postgres.fields import JSONField

#from backend.hume.models import Hume
#from backend.user.models import User


# Create your models here.
#class Device(models.Model):
#    hume = models.ForeignKey(Hume, on_delete=models.CASCADE, primary_key=False)

#    name = models.CharField(null=True, blank=True, max_length=100)

#    type = models.IntegerField(editable=False)

#    heartbeat = models.DateTimeField(auto_now_add=True)


#class DeviceConfiguration(models.Model):
#    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)

#    configuration = JSONField()

#    last_update = models.DateTimeField(auto_now=True)
#    updated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, primary_key=False)
