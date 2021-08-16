import uuid
import random

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
from backend.home.models import Home, Room
from backend.user.models import User
from backend.device.test_defs import (  # noqa
    BASIC_LED_CAPS,
    HUME_UUID,
    DEVICE_UUID_1,
    DEVICE_UUID_2,
    DEVICE_UUID_3,
)


def create_dummy_device(hume: Hume):
    """
    Instantiates a new dummy device, useful helper for testing access control,
    not so much for DB integrity and modelling accuracy.

    :returns: Device
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
    test_case.assertEqual(
        device.description,
        device_spec["description"]
    )
    test_case.assertEqual(device.category, device_spec["category"])
    test_case.assertEqual(device.type, device_spec["type"])


class ModelTests(TestCase):
    """Verifies behavior of Device models and instantiation helpers"""

    @classmethod
    def setUpClass(cls):
        """
        CALLED PER TEST CASE!
        """
        super().setUpClass()
        Hume.objects.create(uuid=HUME_UUID)

    def test_create_stateful_device(self):
        """Verify a Basic LED device can be created without problems."""
        create_device(Hume.objects.get(uuid=HUME_UUID), BASIC_LED_CAPS)
        device = Device.objects.get(uuid=DEVICE_UUID_1)
        device_state_group = DeviceStateGroup.objects.get(
            device=device, group_id=0)
        on, off = DeviceState.objects.filter(
            device_state_group=device_state_group)
        self.assertEqual(on.state_id, 1)
        self.assertEqual(off.state_id, 0)
        verify_device_fields(self, device, BASIC_LED_CAPS)


class DevicesApi(TestCase):
    """Create device instances, in conjunction with an attach sequence."""

    DEVICES_URL = "/api/humes/{}/devices"

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

    def test_create_device_api(self):
        """Verify the create device API works when used correctly"""
        res = self.client.post(DevicesApi.DEVICES_URL.format(HUME_UUID),
                               BASIC_LED_CAPS)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_device_failed_user_not_a_hume(self):
        """
        Verify that users that are not related to HUMEs cannot create devices.
        """
        user = User.objects.create_user(
            "bad@person.com", "pw", "Hans", "Grüber")
        client = APIClient()
        client.login(username=user.email, password="pw")
        res = client.post(DevicesApi.DEVICES_URL.format(HUME_UUID),
                          BASIC_LED_CAPS)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class RoomDeviceGetApi(TestCase):
    """Get devices based on input Room."""

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
        self.home.save()
        self.room = Room.objects.create(name="room", home=self.home)

        self.hume = Hume.objects.create(uuid=uuid.uuid4(),
                                        home=self.home)

    def test_get_devices_of_no_room(self):
        """
        Verify devices can be gotten when they do not belong to a specific
        room.
        """
        create_dummy_device(self.hume)

        res = self.client.get(f"/api/homes/{self.home.id}/devices")

        # 1 result expected
        self.assertEqual(len(res.data), 1)

    def test_get_devices_of_a_room(self):
        """
        Verify devices can be gotten when associated with a room.
        """
        device = create_dummy_device(self.hume)
        device.room = self.room
        device.save()

        res = self.client.get(f"/api/rooms/{self.room.id}/devices")

        self.assertEqual(len(res.data), 1)

    def test_get_devices_do_not_leak_between_rooms_of_a_home(self):
        """
        Verify that if there are several devices, each belonging to a
        different, or no, room, a GET directed at a particular room/
        no room does not result in getting devices of a room that was
        not pointed out.
        """
        device_1 = create_dummy_device(self.hume)
        device_1.room = self.room
        device_1.save()

        device_2 = create_dummy_device(self.hume)
        room_2 = Room.objects.create(home=self.home, name="room2")
        device_2.room = room_2
        device_2.save()

        # One last with no room assigned
        device_3 = create_dummy_device(self.hume)

        # Get the device with self.room assigned:
        res = self.client.get(f"/api/rooms/{self.room.id}/devices")
        [device] = res.data

        self.assertEqual(device["uuid"], device_1.uuid)

        # Get the device with room_2 assigned:
        res = self.client.get(f"/api/rooms/{room_2.id}/devices")
        [device] = res.data

        self.assertEqual(device["uuid"], device_2.uuid)

        # Get the device with no room assigned:
        res = self.client.get(f"/api/homes/{self.home.id}/devices")
        [device] = res.data

        self.assertEqual(device["uuid"], device_3.uuid)

    def test_get_devices_no_user_leakage(self):
        """
        Verify that devices that belong to one user cannot be gotten by
        another user who is not part of the device's home user list.
        """
        # Device with room assigned
        device = create_dummy_device(self.hume)
        device.room = self.room
        device.save()

        # Device with no room assigned, belonging to the Home.
        create_dummy_device(self.hume)

        User.objects.create_user(email="t@t.se", password="password")
        client = APIClient()
        client.login(username="t@t.se", password="password")

        res = client.get(f"/api/homes/{self.home.id}/devices")
        self.assertEqual(len(res.data), 0)

        res = client.get(f"/api/rooms/{self.room.id}/devices")
        self.assertEqual(len(res.data), 0)


class DeviceRoomAssignmentAPI(TestCase):
    """Test the room assignment endpoint."""

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
        self.home.save()
        self.room = Room.objects.create(name="room", home=self.home)

        self.hume = Hume.objects.create(uuid=uuid.uuid4(),
                                        home=self.home)

    def test_assign_device_to_a_room(self):
        """Verify device room assignment works."""
        device = create_dummy_device(self.hume)

        self.client.patch(f"/api/devices/{device.uuid}/change-room",
                          {"new_id": self.room.id, "old_id": None})

        device = Device.objects.get(uuid=device.uuid)
        self.assertEqual(device.room.id, self.room.id)

    def test_assign_device_to_a_home(self):
        """Verify assigning a device no room works."""
        device = create_dummy_device(self.hume)
        device.room = self.room
        device.save()

        self.client.patch(f"/api/devices/{device.uuid}/change-room",
                          {"new_id": None, "old_id": self.room.id})

        device = Device.objects.get(uuid=device.uuid)

        self.assertEqual(device.room, None)
