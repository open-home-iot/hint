from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.device.models import (
    Device,
    DeviceDataSource,
    DeviceReading,
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


class DeviceDataSourceAdmin(ModelAdmin):
    model = DeviceDataSource
    list_display = ('id', )


class DeviceReadingAdmin(ModelAdmin):
    model = DeviceReading
    list_display = ('id', )


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceStateGroup, DeviceStateGroupAdmin)
admin.site.register(DeviceState, DeviceStateAdmin)
admin.site.register(DeviceDataSource, DeviceDataSourceAdmin)
admin.site.register(DeviceReading, DeviceReadingAdmin)
