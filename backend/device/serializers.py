from rest_framework import serializers

from backend.device.models import Device


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('hume', 'is_attached', 'room', 'uuid', 'name',
                  'description', 'category', 'type', 'custom_type_name',
                  'parent')
