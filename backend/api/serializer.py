from django.contrib.auth.models import User, Group

from rest_framework import serializers

from api.models import Info


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


class PictureSerializer(serializers.Serializer):

    picture_name = serializers.CharField(max_length=50)
