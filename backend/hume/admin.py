from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.hume.models import ValidHume


class HumeAdmin(ModelAdmin):
    model = ValidHume


admin.site.register(ValidHume, HumeAdmin)
