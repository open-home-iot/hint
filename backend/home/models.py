from django.db import models

from backend.user.models import User


class Home(models.Model):
    # pylint: disable=missing-class-docstring

    users = models.ManyToManyField(User)
    name = models.CharField(max_length=50, blank=False)


class Room(models.Model):
    # pylint: disable=missing-class-docstring

    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
