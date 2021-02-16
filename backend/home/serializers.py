from rest_framework import serializers

from backend.home.models import Home, Room


class HomeSerializer(serializers.ModelSerializer):
    # pylint: disable=missing-class-docstring,too-few-public-methods

    class Meta:
        model = Home
        fields = ('id', 'name')


class RoomSerializer(serializers.ModelSerializer):
    # pylint: disable=missing-class-docstring,too-few-public-methods

    class Meta:
        model = Room
        fields = ('id', 'home', 'name')
