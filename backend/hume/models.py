from django.db import models

from backend.user.models import User
from backend.home.models import Home


class Hume(models.Model):
    """Models a HUME which belongs to a home."""

    # HUME originated info
    uuid = models.UUIDField(unique=True, primary_key=True)
    heartbeat = models.DateTimeField(auto_now_add=True)

    # HINT-allocated user account for HUME requests
    hume_user = models.OneToOneField(User,
                                     on_delete=models.CASCADE,
                                     null=True)

    # User specified
    home = models.ForeignKey(Home,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    name = models.CharField(blank=True, max_length=50)


class ValidHume(models.Model):
    """
    A ValidHume instance contains a valid HUME UUID, for each HUME there must
    exist a ValidHume.
    """

    uuid = models.UUIDField(primary_key=True)
