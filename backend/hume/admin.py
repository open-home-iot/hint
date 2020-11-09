from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.hume.models import Hume, ValidHume


class ValidHumeAdmin(ModelAdmin):
    model = ValidHume
    list_display = ('uuid', )


class HumeAdmin(ModelAdmin):
    model = Hume
    list_display = ('uuid', )


admin.site.register(ValidHume, ValidHumeAdmin)
admin.site.register(Hume, HumeAdmin)
