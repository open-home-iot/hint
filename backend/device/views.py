from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from backend.device.models import Device, create_device
from backend.device.serializers import DeviceSerializer
from backend.home.models import Room


class Devices(views.APIView):
    """
    Devices API, used for creating new devices.
    """

    def post(self, request, format=None):
        """
        Create a new device.
        """
        print(request.data)

        return Response(status=status.HTTP_201_CREATED)


###############################################################################
# AJAX VIEWS
###############################################################################
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
    """Get devices related to a home, unassigned a room."""

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


class ChangeDeviceRoom(views.APIView):
    """Change the room a device belongs to."""

    def patch(self, request, device_uuid, format=None):
        """
        Change which room a device belongs to.
        """
        try:
            device = Device.objects.get(uuid=device_uuid)

            room = None
            if request.data["new_id"] is not None:
                room = Room.objects.get(id=request.data["new_id"])

            device.room = room
            device.save()
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
