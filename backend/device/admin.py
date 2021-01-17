from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.device.models import (
    Device,
    DeviceAction,
    DeviceDataSource,
    DeviceReading
)


class DeviceAdmin(ModelAdmin):
    model = Device
    list_display = ('uuid', )


class DeviceActionAdmin(ModelAdmin):
    model = DeviceAction
    list_display = ('id', )


class DeviceDataSourceAdmin(ModelAdmin):
    model = DeviceDataSource
    list_display = ('id', )


class DeviceReadingAdmin(ModelAdmin):
    model = DeviceReading
    list_display = ('id', )


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceAction, DeviceActionAdmin)
admin.site.register(DeviceDataSource, DeviceDataSourceAdmin)
admin.site.register(DeviceReading, DeviceReadingAdmin)
