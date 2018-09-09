from django.db import models
from django.contrib.auth import models as auth_models


# Create your models here.
class Hume(models.Model):
    users = models.ManyToManyField(auth_models.User)

    name = models.CharField(null=True, blank=True, max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    is_paired = models.BooleanField(default=False)
    is_dummy = models.BooleanField(default=False)

    heartbeat = models.DateTimeField(auto_now_add=True)


class HumeUser(auth_models.User):
    related_hume = models.OneToOneField(Hume, on_delete=models.CASCADE, primary_key=True)

    hume_auth_token = models.CharField(null=True, blank=True, max_length=100)
