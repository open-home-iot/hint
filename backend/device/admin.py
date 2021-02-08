from django.contrib import admin
from django.contrib.admin import ModelAdmin

from backend.device.models import (
    Device,
    DeviceDataSource,
    DeviceReading
)


class DeviceAdmin(ModelAdmin):
    model = Device
    list_display = ('uuid', )


class DeviceDataSourceAdmin(ModelAdmin):
    model = DeviceDataSource
    list_display = ('id', )


class DeviceReadingAdmin(ModelAdmin):
    model = DeviceReading
    list_display = ('id', )


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceDataSource, DeviceDataSourceAdmin)
admin.site.register(DeviceReading, DeviceReadingAdmin)
