from django.db import models

from backend.user.models import User


class Home(models.Model):
    """Models a home which has rooms and HUMEs."""

    users = models.ManyToManyField(User)
    name = models.CharField(max_length=50, blank=False)
