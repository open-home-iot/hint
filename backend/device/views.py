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
            # Requested room ID
            room__id=room_id,
            # Does the device exist in a home the user owns?
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
            # No room assignment
            room=None,
            # Requested home ID
            hume__home__id=home_id,
            # Does the device exist in a home the user owns?
            hume__home__users__id=request.user.id
        )

        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
