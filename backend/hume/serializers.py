from rest_framework import serializers

from .models import Hume


class HumeSerializer(serializers.ModelSerializer):
    # pylint: disable=missing-class-docstring,too-few-public-methods

    class Meta:
        model = Hume
        fields = ('uuid', 'heartbeat', 'name', 'hume_user')
