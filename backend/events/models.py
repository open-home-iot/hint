from django.db import models


class EventStatus(models.Model):
    alarm = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Event Statuses'
