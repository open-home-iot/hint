import uuid
import random
import copy

from unittest.mock import patch, Mock, ANY

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from backend.device.models import (
    Device,
    DeviceStateGroup,
    DeviceState,
    create_device,
)
from backend.hume.models import Hume
from backend.home.models import Home
from backend.user.models import User
from backend.device.test_defs import (  # noqa
    BASIC_LED_CAPS,
    HUME_UUID,
    DEVICE_UUID_1,
    DEVICE_UUID_2,
    DEVICE_UUID_3,
)


def create_dummy_device(hume: Hume) -> Device:
    """
    Instantiates a new dummy device, useful helper for testing access control,
    not so much for DB integrity and modelling accuracy.
    """
    device = Device.objects.create(
        hume=hume,
        uuid=str(uuid.uuid4()),
        name="dummy_device",
        category=random.choice(Device.Category.CHOICES)[0],
        type=random.choice(Device.Type.CHOICES)[0]
    )
    return device


def verify_device_fields(test_case: TestCase, device, device_spec):
    """
    Compares the input device instance and device spec and checks that the
    correct objects have been created.

    :param test_case: test case instance
    :type device: Device
    :type device_spec: dict
    """
    test_case.assertEqual(str(device.uuid), device_spec["uuid"])
    test_case.assertEqual(device.name, device_spec["name"])
    test_case.assertEqual(device.category, device_spec["category"])
    test_case.assertEqual(device.type, device_spec["type"])


class DeviceModel(TestCase):
    """Verifies behavior of Device models and instantiation helpers"""

    def setUp(self):
        """
        CALLED PER TEST CASE!
        """
        super().setUpClass()
        self.hume = Hume.objects.create(uuid=HUME_UUID)
        hume_user = User.objects.create_hume_user(HUME_UUID, "pw")
        self.hume.hume_user = hume_user
        self.hume.save()

    def test_create_stateful_device(self):
        """Verify a Basic LED device can be created without problems."""
        create_device(self.hume, copy.deepcopy(BASIC_LED_CAPS))

        device = Device.objects.get(uuid=DEVICE_UUID_1)
        device_state_group = DeviceStateGroup.objects.get(
            device=device, group_id=0)
        on, off = DeviceState.objects.filter(
            device_state_group=device_state_group)

        self.assertEqual(on.state_id, 1)
        self.assertEqual(off.state_id, 0)
        verify_device_fields(self, device, BASIC_LED_CAPS)

    def test_cascade(self):
        """
        Verify a device is deleted when its hume is deleted.
        """
        create_device(self.hume, copy.deepcopy(BASIC_LED_CAPS))

        device = Device.objects.get(uuid=DEVICE_UUID_1)
        verify_device_fields(self, device, BASIC_LED_CAPS)

        self.hume.delete()

        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(uuid=DEVICE_UUID_1)

    @patch('backend.device.signal_handlers.producer')
    def test_signal(self, producer_mock):
        """
        Ensure a deleted device results in a message sent to the device's
        hume.
        """
        create_device(self.hume, copy.deepcopy(BASIC_LED_CAPS))

        device = Device.objects.get(uuid=DEVICE_UUID_1)
        verify_device_fields(self, device, BASIC_LED_CAPS)

        device.delete()
        producer_mock.detach.assert_called_with(self.hume.uuid, DEVICE_UUID_1)


class DevicesApi(TestCase):

    URL = "/api/humes/{}/devices"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Hume.objects.create(uuid=HUME_UUID)
        User.objects.create_hume_user(HUME_UUID, "pw")

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.login(
            username=f"{HUME_UUID.replace('-', '')}@fake.com", password="pw"
        )

    @patch('backend.device.views.async_to_sync')
    def test_create_device_api(self, async_to_sync):
        """Verify the create device API works when used correctly"""
        sync_version = Mock()
        async_to_sync.return_value = sync_version

        res = self.client.post(DevicesApi.URL.format(HUME_UUID),
                               BASIC_LED_CAPS)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        sync_version.assert_called_with(HUME_UUID, ANY)

    @patch('backend.device.views.async_to_sync')
    def test_create_device_failed_user_not_a_hume(self, async_to_sync):
        """
        Verify that users that are not related to HUMEs cannot create devices.
        """
        sync_version = Mock()
        async_to_sync.return_value = sync_version

        user = User.objects.create_user(
            "bad@person.com", "pw", "Hans", "Grüber")
        client = APIClient()
        client.login(username=user.email, password="pw")
        res = client.post(DevicesApi.URL.format(HUME_UUID),
                          BASIC_LED_CAPS)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        sync_version.assert_not_called()


class HomeDevicesApi(TestCase):

    URL = "/api/homes/{}/devices"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        User.objects.create_user(email="suite@t.se", password="pw")

    def setUp(self):
        """
        Create shared test case data.
        """
        self.client = APIClient()
        self.client.login(username="suite@t.se", password="pw")

        self.home = Home.objects.create(name="home")
        self.home.users.add(User.objects.get(email="suite@t.se"))

        self.hume = Hume.objects.create(uuid=uuid.uuid4(),
                                        home=self.home)

    def test_get_home_devices(self):
        """
        Verify devices can be gotten based on a home id.
        """
        create_dummy_device(self.hume)

        res = self.client.get(HomeDevicesApi.URL.format(self.home.id))

        # 1 result expected
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_home_devices_no_inter_home_leakage(self):
        """
        Verify devices do not leak between home instances.
        """
        create_dummy_device(self.hume)

        # Create a second hume for a second home
        hume_2 = Hume.objects.create(uuid=uuid.uuid4(),
                                     home=Home.objects.create(name="home2"))
        device_2 = create_dummy_device(hume_2)

        res = self.client.get(HomeDevicesApi.URL.format(self.home.id))
        [device] = res.data  # expect only 1 result

        # Should not match
        self.assertNotEqual(device["uuid"], device_2.uuid)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_home_devices_no_user_leakage(self):
        """
        Verify a user who is not associated with the device's home cannot
        fetch it throught the home devices API.
        """
        User.objects.create_user(email="t@t.se", password="pw")
        client = APIClient()
        client.login(username="t@t.se", password="pw")

        res = client.get(HomeDevicesApi.URL.format(self.home.id))

        self.assertEqual(len(res.data), 0)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class DeviceActionApi(TestCase):

    URL = "/api/homes/{}/humes/{}/devices/{}/action"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        User.objects.create_user(email="suite@t.se", password="pw")

    def setUp(self):
        """
        Create shared test case data.
        """
        self.client = APIClient()
        self.client.login(username="suite@t.se", password="pw")

        self.home = Home.objects.create(name="home")
        self.home.users.add(User.objects.get(email="suite@t.se"))

        self.hume = Hume.objects.create(uuid=uuid.uuid4(),
                                        home=self.home)

    @patch('backend.device.views.producer')
    def test_stateful_device_action(self, producer_mock):
        """
        Verify the device action API accepts stateful device actions.
        """
        create_device(self.hume, copy.deepcopy(BASIC_LED_CAPS))
        device = Device.objects.get(uuid=DEVICE_UUID_1)
        device_state_kwargs = {"device_state_group_id": 0, "device_state": 0}

        res = self.client.post(
            DeviceActionApi.URL.format(
                self.home.id, self.hume.uuid, device.uuid
            ), device_state_kwargs
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        producer_mock.send_device_action.assert_called_with(
            str(self.hume.uuid), str(device.uuid), **device_state_kwargs
        )

    def test_device_action_unauthorized_user(self):
        """
        Verify a user that does not own a device cannot ask to execute its
        actions.
        """
        device = create_dummy_device(self.hume)

        User.objects.create_user(email="t@t.se", password="pw")
        client = APIClient()
        client.login(username="t@t.se", password="pw")

        res = client.post(DeviceActionApi.URL.format(
            self.home.id, self.hume.uuid, device.uuid)
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    @patch("backend.device.views.producer")
    def test_device_action_fails_no_such_device(self, producer_mock):
        """
        Verify that all URL pieces matter in pointing out which device should
        execute and action.
        """
        device = create_dummy_device(self.hume)

        # Bogus home ID
        res = self.client.post(DeviceActionApi.URL.format(
            1337, self.hume.uuid, device.uuid
        ))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Bogus Hume UUID
        res = self.client.post(DeviceActionApi.URL.format(
            self.home.id, str(uuid.uuid4()), device.uuid
        ))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Bogus device UUID
        res = self.client.post(DeviceActionApi.URL.format(
            self.home.id, self.hume.uuid, str(uuid.uuid4())
        ))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Bogus user
        user = User.objects.create_user(email="t@t.se", password="pw")
        client = APIClient()
        client.login(username=user.email, password="pw")
        res = client.post(DeviceActionApi.URL.format(
            self.home.id, self.hume.uuid, device.uuid
        ))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        producer_mock.send_device_action.assert_not_called()
