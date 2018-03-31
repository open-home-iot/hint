from django.db import models


class Info(models.Model):
    version = models.IntegerField()
    message = models.CharField(max_length=255)
