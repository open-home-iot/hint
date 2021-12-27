from rest_framework import serializers

from backend.home.models import Home


class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Home
        fields = ('id', 'name')
