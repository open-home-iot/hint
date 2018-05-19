from django.contrib.auth.models import User, Group

from rest_framework import serializers

from api.models import Info

from surveillance.models import AlarmHistory


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('url', 'name')


class InfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Info
        fields = ('url', 'version', 'message')


class AlarmHistorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AlarmHistory
        fields = ('date',)
