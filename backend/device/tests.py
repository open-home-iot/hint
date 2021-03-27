import uuid
import random

from django.test import TestCase
from rest_framework.test import APIClient

from backend.device.models import (
    Device,
    DeviceDataSource,
    DataType,
    create_device
)
from backend.hume.models import Hume
from backend.home.models import Home, Room
from backend.user.models import User


HUME_UUID = "9cb37270-69f5-4dc0-9fd5-7183da5ffc19"
DEVICE_UUID_1 = "e2bf93b6-9b5d-4944-a863-611b6b6600e7"
DEVICE_UUID_2 = "e2bf93b6-9b5d-4944-a863-611b6b6600e1"
DEVICE_UUID_3 = "e2bf93b6-9b5d-4944-a863-611b6b6600e2"


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


def verify_device_fields(test_case, device, device_spec):
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


def verify_device_data_sources(test_case, data_sources, device_spec):
    """
    Compares the input data source instances to the device spec.

    :param test_case: test case instance
    :type data_sources:
    :type device_spec:
    """
    spec_sources = device_spec["data_sources"]
    test_case.assertEqual(len(data_sources), len(spec_sources))

    for spec_source in spec_sources:
        match_found = False

        for source_instance in data_sources:
            if source_instance.name == spec_source["name"]:
                test_case.assertTrue(
                    source_instance.data_type == spec_source["data_type"]
                )
                match_found = True
                break

        if not match_found:
            test_case.fail(
                f"No matching data source created for: {spec_source}"
            )


class ModelTests(TestCase):
    """Verifies behavior of Device models and instantiation helpers"""

    def setUp(self):
        """
        CALLED PER TEST CASE!
        """
        self.hume = Hume.objects.create(uuid=HUME_UUID)

    def test_create_single_data_source_sensor(self):
        """
        Test creating model instances for a single data source sensor device.
        """
        device_spec = {
            "uuid": DEVICE_UUID_1,
            "name": "Simple sensor",
            "description": "Some description",
            "category": Device.Category.SENSOR,
            "type": Device.Type.THERMOMETER,
            "data_sources": [
                {
                    "name": "Temperature",
                    "data_type": DataType.INT
                }
            ]
        }
        create_device(self.hume, device_spec)

        device = Device.objects.get(uuid=DEVICE_UUID_1)
        self.assertEqual(str(device.hume.uuid), self.hume.uuid)
        verify_device_fields(self, device, device_spec)

        data_sources = DeviceDataSource.objects.filter(device=device)
        verify_device_data_sources(self, data_sources, device_spec)

    def test_create_thermometer(self):
        """
        Test creating model instances required for a thermometer device.
        """
        # Thermometer with two data sources and corresponding actions to read
        device_spec = {
            "uuid": DEVICE_UUID_1,
            "name": "THERMO X2",
            "description": "Combined Thermometer and Humidity sensor.",
            "category": Device.Category.SENSOR,
            "type": Device.Type.THERMOMETER,
            "data_sources": [
                {
                    "name": "Temperature",
                    "data_type": DataType.FLOAT
                },
                {
                    "name": "Humidity",
                    "data_type": DataType.PERC_FLOAT
                },
            ]
        }
        create_device(self.hume, device_spec)

        device = Device.objects.get(uuid=DEVICE_UUID_1)
        self.assertEqual(str(device.hume.uuid), self.hume.uuid)
        verify_device_fields(self, device, device_spec)

        data_sources = DeviceDataSource.objects.filter(device=device)
        verify_device_data_sources(self, data_sources, device_spec)


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
