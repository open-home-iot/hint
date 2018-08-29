from django.db import models
from django.contrib.auth import models as auth_models


# Create your models here.
class Hume(models.Model):
    users = models.ManyToManyField(auth_models.User)

    name = models.CharField(null=True, blank=True, max_length=100)
    ip_address = models.IPAddressField(null=True, blank=True)

    is_paired = models.BooleanField(null=False, blank=False, default=False)
    is_dummy = models.BooleanField(null=False, blank=False, default=False)

    heartbeat = models.DateTimeField(null=True, blank=True)


class HumeUser(auth_models.User):
    hume = models.OneToOneField(Hume, on_delete=models.CASCADE, primary_key=True)

    hume_auth_token = models.CharField(null=True, blank=True, max_length=100)

