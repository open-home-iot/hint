from django.db import models

from backend.home.models import Home


class Hume(models.Model):
    # HUME originated info
    uuid = models.UUIDField(unique=True)
    ip_address = models.GenericIPAddressField()
    heartbeat = models.DateTimeField(auto_now_add=True)

    # HINT info
    is_paired = models.BooleanField(default=False)

    # User specified
    home = models.ForeignKey(Home, on_delete=models.CASCADE, null=True)
    name = models.CharField(blank=True, max_length=50)
