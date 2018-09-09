from django.test import TestCase
from django.contrib.auth import models as auth_models

from hume.models import Hume
from device.models import DeviceConfiguration, Device


# Create your tests here.
class HumeDeleted(TestCase):
    def setUp(self):
        hume = Hume.objects.create(pk=1)
        Device.objects.create(hume=hume, type=1)

    def test_hume_deleted(self):
        hume = Hume.objects.get(pk=1)
        hume.delete()

        self.assertEqual(0, len(Device.objects.all()))


class DeviceDeleted(TestCase):
    def setUp(self):
        hume = Hume.objects.create()

        device = Device.objects.create(pk=1, hume=hume, type=1)

        DeviceConfiguration.objects.create(pk=1, device=device, configuration={'1': 1})

    def test_device_deleted(self):
        device = Device.objects.get(pk=1)
        device.delete()

        self.assertEqual(0, len(DeviceConfiguration.objects.all()))

    def test_user_deleted(self):
        user = auth_models.User(pk=1)
        user.save()

        device_config = DeviceConfiguration.objects.get(pk=1)
        device_config.updated_by = user
        device_config.save()

        user = auth_models.User.objects.get(pk=1)
        user.delete()

        self.assertEqual(1, len(DeviceConfiguration.objects.all()))
