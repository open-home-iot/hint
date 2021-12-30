from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from backend.device.models import Device, create_device
from backend.device.serializers import DeviceSerializer
from backend.hume.models import Hume
from backend.broker.defs import MessageType
from backend.broker import producer
from backend.user.permissions import IsHume


###############################################################################
# HUME VIEWS
###############################################################################
class Devices(views.APIView):
    """Devices API, used for creating new devices."""

    permission_classes = [IsAuthenticated, IsHume]

    @staticmethod
    def post(request, hume_uuid):
        """
        Create a new device.
        """
        create_device(Hume.objects.get(uuid=hume_uuid), request.data)

        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                hume_uuid,
                {
                    "type": "hume.event",
                    "hume_uuid": hume_uuid,
                    "event_type": MessageType.ATTACH_DEVICE,
                    "content": {
                        "identifier": request.data["identifier"],
                        "success": True,
                    },
                }
            )
        except Exception:  # noqa
            # ignore message sending errors to avoid HUME-HINT mismatches
            pass

        return Response(status=status.HTTP_201_CREATED)


###############################################################################
# AJAX VIEWS
###############################################################################
class HomeDevices(views.APIView):
    """Get devices related to a home."""

    @staticmethod
    def get(request, home_id):
        """
        Get all home devices.
        """
        devices = Device.objects.filter(
            # Requested home ID
            hume__home__id=home_id,
            # Does the device exist in a home the user owns?
            hume__home__users__id=request.user.id
        )

        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeviceSingle(views.APIView):
    """Operations on single device instances."""

    @staticmethod
    def delete(request, home_id, hume_uuid, device_uuid):
        """Delete a device."""
        try:
            device = Device.objects.get(uuid=device_uuid,
                                        hume__uuid=hume_uuid,
                                        hume__home__id=home_id,
                                        hume__home__users__id=request.user.id)
            device.delete()
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)


class DeviceAction(views.APIView):
    """Execute a device action."""

    @staticmethod
    def post(request, home_id, hume_uuid, device_uuid):
        """
        Execute a device action, POST since the device's state may change.
        """
        try:
            Device.objects.get(uuid=device_uuid,
                               hume__uuid=hume_uuid,
                               hume__home__id=home_id,
                               hume__home__users__id=request.user.id)
            producer.send_device_action(hume_uuid, device_uuid, **request.data)
            return Response(status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
