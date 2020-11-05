from django.db import models

from backend.user.models import User
from backend.home.models import Home


class Hume(models.Model):
    # HUME originated info
    uuid = models.UUIDField(unique=True)
    heartbeat = models.DateTimeField(auto_now_add=True)

    # HINT info
    is_paired = models.BooleanField(default=False)

    # User specified
    home = models.ForeignKey(Home, on_delete=models.CASCADE, null=True)
    name = models.CharField(blank=True, max_length=50)


class HumeUser(User):
    hume = models.ForeignKey(Hume, on_delete=models.CASCADE)


class ValidHume(models.Model):
    uuid = models.UUIDField(unique=True)
    taken = models.BooleanField(default=False)
