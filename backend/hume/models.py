from django.db import models

from backend.user.models import User


#class Hume(models.Model):
#    users = models.ManyToManyField(User)

#    name = models.CharField(null=True, blank=True, max_length=100)
#    ip_address = models.GenericIPAddressField(null=True, blank=True)

#    heartbeat = models.DateTimeField(auto_now_add=True)


#class HumeUser(models.Model):
#    related_hume = models.OneToOneField(Hume,
#                                        on_delete=models.CASCADE,
#                                        primary_key=True)
#
#    hume_auth_token = models.CharField(null=True, blank=True, max_length=100)
#    pass
