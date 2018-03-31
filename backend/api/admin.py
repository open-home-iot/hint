from django.contrib import admin
from django.contrib.admin import ModelAdmin

from api.models import Info


admin.site.register(Info, ModelAdmin)
