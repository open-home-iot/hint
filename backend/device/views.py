from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from backend.device.models import Device, create_device
from backend.device.serializers import DeviceSerializer
from backend.home.models import Room
from backend.hume.models import Hume
from backend.broker.defs import ATTACH_DEVICE
from backend.broker import producer


class Devices(views.APIView):
    """
    Devices API, used for creating new devices.
    """

    def post(self, request, hume_uuid, format=None):
        """
        Create a new device.
        """
        if request.user.is_hume:
            create_device(Hume.objects.get(uuid=hume_uuid), request.data)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                hume_uuid,
                {
                    "type": "hume.event",
                    "hume_uuid": hume_uuid,
                    "event_type": ATTACH_DEVICE,
                    "content": "",
                }
            )

            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


###############################################################################
# AJAX VIEWS
###############################################################################
class RoomDevices(views.APIView):
    """Get devices related to a Room."""

    def get(self, request, home_id, room_id, format=None):
        """
        Get all device of a specified room.
        """
        devices = Device.objects.filter(
            # Requested home & room ID
            room__id=room_id,
            hume__home__id=home_id,
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

    def patch(self, request, home_id, hume_uuid, device_uuid, format=None):
        """
        Change which room a device belongs to.
        """
        try:
            device = Device.objects.get(uuid=device_uuid,
                                        hume__home__users__id=request.user.id)

            room = None
            if request.data["new_id"] is not None:
                room = Room.objects.get(id=request.data["new_id"],
                                        home__users__id=request.user.id)

            device.room = room
            device.save()
        except (Device.DoesNotExist, Room.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceAction(views.APIView):
    """Execute a device action."""

    def post(self, request, hume_uuid, device_uuid, format=None):
        try:
            Device.objects.get(uuid=device_uuid,
                               hume__uuid=hume_uuid,
                               hume__home__users__id=request.user.id)
            producer.send_device_action(hume_uuid, device_uuid, **request.data)
            return Response(status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
