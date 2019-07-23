from django.test import TestCase
from django.contrib.auth import models as auth_models
from django.db import transaction
from django.db.utils import IntegrityError

from psycopg2 import IntegrityError as PIntegrityError

from backend.hume.models import Hume
from backend.device.models import DeviceConfiguration, Device


# Create your tests here.
class Delete(TestCase):
    def setUp(self):
        """Create shared test case data, what's created here needs to be torn down in tearDown()."""
        hume = Hume.objects.create(pk=1)
        Device.objects.create(pk=1, hume=hume, type=1)

    def tearDown(self):
        """Clear all created data from setUp()."""
        for user in auth_models.User.objects.all():
            user.delete()

        for hume in Hume.objects.all():
            hume.delete()

        for device in Device.objects.all():
            device.delete()

    def test_hume_deleted(self):
        """Associated devices get deleted when the HUME is deleted."""
        hume = Hume.objects.get(pk=1)
        hume.delete()

        self.assertEqual(0, len(Device.objects.all()))

    def test_device_deleted(self):
        """A device configuration gets deleted when the device is deleted."""
        device = Device.objects.get(pk=1)
        DeviceConfiguration.objects.create(pk=1, device=device, configuration={'1': 1})

        device.delete()

        self.assertEqual(0, len(DeviceConfiguration.objects.all()))

    def test_user_deleted(self):
        """A device configuration does not get deleted when the last updating user gets deleted."""
        user = auth_models.User(pk=1, username='Klaus')
        user.save()
        user_two = auth_models.User(pk=2, username='Moike')
        user_two.save()

        # Add two users not to trigger a delete of the HUME when the user is cleared.
        hume = Hume.objects.get(pk=1)
        hume.users.add(user)
        hume.users.add(user_two)

        device = Device.objects.get(pk=1)
        DeviceConfiguration.objects.create(updated_by=user, device=device, configuration={'1': 1})

        device_config = DeviceConfiguration.objects.get(pk=device.pk)
        device_config.updated_by = user
        device_config.save()

        user = auth_models.User.objects.get(pk=1)
        user.delete()

        self.assertEqual(1, len(DeviceConfiguration.objects.all()))


class Create(TestCase):
    def setUp(self):
        """Create shared test case data, what's created here needs to be torn down in tearDown()."""
        hume = Hume.objects.create(pk=1)
        Device.objects.create(pk=1, hume=hume, type=1)

    def tearDown(self):
        """Clear all created data from setUp()."""
        if Hume.objects.filter(pk=1).exists():
            Hume.objects.get(pk=1).delete()

        # Since multi-add is tested.
        for device in Device.objects.all():
            device.delete()

        for config in DeviceConfiguration.objects.all():
            config.delete()

    def test_multiple_devices_per_hume(self):
        hume = Hume.objects.get(pk=1)

        for index in range(2, 5):
            Device.objects.create(pk=index, hume=hume, type=index)

        self.assertEqual(4, len(Device.objects.filter(hume=hume)))

    def test_multiple_configurations_for_one_device(self):
        device = Device.objects.get(pk=1)

        DeviceConfiguration.objects.create(device=device, configuration={'1': 1})

        # Django + the unittest module does not like exceptions during transactions.
        with transaction.atomic():
            try:
                DeviceConfiguration.objects.create(device=device, configuration={'1': 1})
                self.fail('Duplicate configurations were allowed!')

            # Not sure which bloody error it was...
            except IntegrityError or PIntegrityError:
                pass

    def test_adding_a_second_device_and_config(self):
        """Test that relations between configurations and devices as well as users work."""
        hume = Hume.objects.get(pk=1)
        user = auth_models.User.objects.create(pk=1)

        device = Device.objects.get(pk=1)

        device_two = Device.objects.create(pk=2, hume=hume, type=1)

        # Same user for both configurations.
        DeviceConfiguration.objects.create(updated_by=user, device=device, configuration={'1': 1})
        DeviceConfiguration.objects.create(updated_by=user, device=device_two, configuration={'1': 1})

        self.assertEqual(2, len(DeviceConfiguration.objects.all()))
