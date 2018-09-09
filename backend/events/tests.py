from django.test import TestCase

from hume.models import Hume
from device.models import Device
from events.models import Log


# Create your tests here.
class Move(TestCase):
    def setUp(self):
        """Create shared test case data, what's created here needs to be torn down in tearDown()."""
        hume = Hume.objects.create(pk=1)
        device = Device.objects.create(pk=1, hume=hume, type=1)
        Log.objects.create(pk=1, device=device, type=1, value=1)

    def tearDown(self):
        """Clear all created data from setUp()."""
        for hume in Hume.objects.all():
            hume.delete()

        for device in Device.objects.all():
            device.delete()

        for log in Log.objects.all():
            log.delete()

    def test_keeping_logs_after_device_removed(self):
        """Logs can be kept using a dummy device."""
        hume = Hume.objects.get(pk=1)
        dummy = Device.objects.create(pk=2, hume=hume, type=1)

        log = Log.objects.get(pk=1)
        log.device = dummy
        log.save()

        device = Device.objects.get(pk=1)
        device.delete()

        self.assertEqual(1, len(Log.objects.all()))


class Create(TestCase):
    def setUp(self):
        """Create shared test case data, what's created here needs to be torn down in tearDown()."""
        hume = Hume.objects.create(pk=1)
        device = Device.objects.create(pk=1, hume=hume, type=1)
        Log.objects.create(pk=1, device=device, type=1, value=1)

    def tearDown(self):
        """Clear all created data from setUp()."""
        for hume in Hume.objects.all():
            hume.delete()

        for device in Device.objects.all():
            device.delete()

        for log in Log.objects.all():
            log.delete()

    def test_multiple_logs_for_one_device(self):
        """One device can have many logs."""
        device = Device.objects.get(pk=1)

        for index in range(2, 5):
            Log.objects.create(pk=index, device=device, type=1, value=1)

        self.assertEqual(4, len(Log.objects.filter(device=device)))


class Delete(TestCase):
    def setUp(self):
        """Create shared test case data, what's created here needs to be torn down in tearDown()."""
        hume = Hume.objects.create(pk=1)
        device = Device.objects.create(pk=1, hume=hume, type=1)
        Log.objects.create(pk=1, device=device, type=1, value=1)

    def tearDown(self):
        """Clear all created data from setUp()."""
        for hume in Hume.objects.all():
            hume.delete()

        for device in Device.objects.all():
            device.delete()

        for log in Log.objects.all():
            log.delete()

    def test_log_deleted_when_device_deleted(self):
        """Deleting a device deletes only the associated logs with THAT device, not others."""
        hume = Hume.objects.get(pk=1)

        other_device = Device.objects.create(pk=2, hume=hume, type=1)
        Log.objects.create(pk=2, device=other_device, type=1, value=2)

        device = Device.objects.get(pk=1)
        device.delete()

        self.assertEqual(0, len(Log.objects.filter(device=device)))
        self.assertEqual(1, len(Log.objects.all()))
