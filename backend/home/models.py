from django.db import models

from backend.user.models import User


class Home(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=50, blank=False)
