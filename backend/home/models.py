from django.db import models

from backend.user.models import User


class Home(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=50, blank=False)


class Room(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
