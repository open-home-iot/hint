from django.contrib.auth.models import User, Group

from rest_framework import serializers

from api.models import Info

from surveillance.models import AlarmHistory, SurvConfiguration


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


class SurvConfigurationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SurvConfiguration
        fields = ('alarm_state', 'picture_mode')

    def create(self, validated_data):
        print(validated_data)
        answer, created = SurvConfiguration.objects.update_or_create(
            pk=1, # TODO exchange for user reference
            defaults={'alarm_state': validated_data.get('alarm_state', True),
                      'picture_mode': validated_data.get('picture_mode', True)}
        )

        return answer


class AlarmHistorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AlarmHistory
        fields = ('date',)
