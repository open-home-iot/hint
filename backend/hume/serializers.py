from rest_framework import serializers

from .models import Hume


class HumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hume
        fields = ('uuid', 'heartbeat', 'name', 'hume_user')
