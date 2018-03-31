from django.contrib import admin
from django.contrib.admin import ModelAdmin

from events.models import EventStatus


admin.site.register(EventStatus, ModelAdmin)