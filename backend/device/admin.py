from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.device.models import (
    Device,
    DeviceStateGroup,
    DeviceState,
)


class DeviceAdmin(ModelAdmin):
    model = Device
    list_display = ('uuid', )


class DeviceStateGroupAdmin(ModelAdmin):
    model = DeviceStateGroup
    list_display = ('id', )


class DeviceStateAdmin(ModelAdmin):
    model = DeviceState
    list_display = ('id', )


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceStateGroup, DeviceStateGroupAdmin)
admin.site.register(DeviceState, DeviceStateAdmin)
