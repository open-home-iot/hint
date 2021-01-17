from django.test import TestCase

from backend.device.models import (
    Device,
    DeviceDataSource,
    DeviceAction,
    DataType,
    create_device
)
from backend.hume.models import Hume


HUME_UUID = "9cb37270-69f5-4dc0-9fd5-7183da5ffc19"
DEVICE_UUID_1 = "e2bf93b6-9b5d-4944-a863-611b6b6600e7"
DEVICE_UUID_2 = "e2bf93b6-9b5d-4944-a863-611b6b6600e1"
DEVICE_UUID_3 = "e2bf93b6-9b5d-4944-a863-611b6b6600e2"


class ModelTests(TestCase):

    def setUp(self):
        """
        CALLED PER TEST CASE!
        """
        self.hume = Hume.objects.create(uuid=HUME_UUID)

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
                    "id": 0,
                    "name": "Temperature",
                    "data_type": DataType.FLOAT
                },
                {
                    "id": 1,
                    "name": "Humidity",
                    "data_type": DataType.PERC_FLOAT
                },
            ],
            "actions": [
                {
                    "id": 0,
                    "name": "Read temperature",
                    "type": DeviceAction.Type.READ,
                    "data_source": 0,
                },
                {
                    "id": 1,
                    "name": "Read humidity",
                    "type": DeviceAction.Type.READ,
                    "data_source": 1,
                },
            ],
        }
        create_device(self.hume, device_spec)

        device = Device.objects.get(uuid=DEVICE_UUID_1)
        DeviceDataSource.objects.get(device=device, data_source_id=0)
        DeviceDataSource.objects.get(device=device, data_source_id=1)
        action = DeviceAction.objects.get(device=device, action_id=0)
        self.assertEqual(action.data_source.data_source_id, 0)
        action = DeviceAction.objects.get(device=device, action_id=1)
        self.assertEqual(action.data_source.data_source_id, 1)

    def test_create_simplest_device(self):
        """
        Test creating the simplest device, an actuator with only one vanilla
        action.
        """
        # Simple device, one VANILLA action
        device_spec = {
            "uuid": DEVICE_UUID_1,
            "name": "Peckinator",
            "description": "Pecks things.",
            "category": Device.Category.ACTUATOR,
            "type": Device.Type.CUSTOM,
            "custom_type_name": "Pecker",
            "actions": [
                {
                    "id": 0,
                    "name": "Peck",
                    "type": DeviceAction.Type.VANILLA,
                },
            ],
        }
        create_device(self.hume, device_spec)

        device = Device.objects.get(uuid=DEVICE_UUID_1)
        DeviceAction.objects.get(device=device, action_id=0)
