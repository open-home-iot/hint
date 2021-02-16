# pylint: disable=missing-class-docstring
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.home.models import Home, Room


class HomeAdmin(ModelAdmin):
    model = Home
    list_display = ('id', 'name')


class RoomAdmin(ModelAdmin):
    model = Room
    list_display = ('id', 'home', 'name')


admin.site.register(Home, HomeAdmin)
admin.site.register(Room, RoomAdmin)
