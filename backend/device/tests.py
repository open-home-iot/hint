from django.test import TestCase

from backend.device.models import (
    Device,
    DeviceDataSource,
    DataType,
    create_device
)
from backend.hume.models import Hume


HUME_UUID = "9cb37270-69f5-4dc0-9fd5-7183da5ffc19"
DEVICE_UUID_1 = "e2bf93b6-9b5d-4944-a863-611b6b6600e7"
DEVICE_UUID_2 = "e2bf93b6-9b5d-4944-a863-611b6b6600e1"
DEVICE_UUID_3 = "e2bf93b6-9b5d-4944-a863-611b6b6600e2"


def verify_device_fields(tc, device, device_spec):
    """
    Compares the input device instance and device spec and checks that the
    correct objects have been created.

    :param tc: test case instance
    :type device: Device
    :type device_spec: dict
    """
    tc.assertEqual(str(device.uuid), device_spec["uuid"])
    tc.assertEqual(device.name, device_spec["name"])
    tc.assertEqual(
        device.description,
        device_spec["description"]
    )
    tc.assertEqual(device.category, device_spec["category"])
    tc.assertEqual(device.type, device_spec["type"])


def verify_device_data_sources(tc, data_sources, device_spec):
    """
    Compares the input data source instances to the device spec.

    :param tc: test case instance
    :type data_sources:
    :type device_spec:
    """
    spec_sources = device_spec["data_sources"]
    tc.assertEqual(len(data_sources), len(spec_sources))

    for spec_source in spec_sources:
        match_found = False

        for source_instance in data_sources:
            if source_instance.name == spec_source["name"]:
                tc.assertTrue(
                    source_instance.data_type == spec_source["data_type"]
                )
                match_found = True
                break

        if not match_found:
            tc.fail(f"No matching data source created for: {spec_source}")


class ModelTests(TestCase):

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
