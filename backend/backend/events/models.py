from django.db import models


class EventStatus(models.Model):
    alarm = models.BooleanField()