from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from backend.device.models import Device
from backend.device.serializers import DeviceSerializer


class RoomDevices(views.APIView):
    """Get devices related to a Room."""

    def get(self, request, room_id, format=None):
        """
        Get all device of a specified room.
        """
        devices = Device.objects.filter(
            room__id=room_id,
            hume__home__users__id=request.user.id
        )

        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HomeDevices(views.APIView):
    """Get devices related to a Room."""

    def get(self, request, home_id, format=None):
        """
        Get all device of a specified room.
        """
        devices = Device.objects.filter(
            room=None,
            hume__home__id=home_id,
            hume__home__users__id=request.user.id
        )

        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
