from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.home.models import Home


class HomeAdmin(ModelAdmin):
    model = Home
    list_display = ('id', 'name')


admin.site.register(Home, HomeAdmin)
