from rest_framework import serializers

from backend.device.models import Device, DeviceStateGroup, DeviceState


class DeviceStateGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceStateGroup
        fields = ('group_id', 'name',)


class DeviceStateSerializer(serializers.ModelSerializer):

    group = DeviceStateGroupSerializer()

    class Meta:
        model = DeviceState
        fields = ('group', 'state_id', 'name',)


class DeviceSerializer(serializers.ModelSerializer):

    states = DeviceStateSerializer(many=True)

    class Meta:
        model = Device
        fields = ('hume',
                  'uuid',
                  'name',
                  'description',
                  'category_name',
                  'type_name',
                  'states',)
