from backend.device.models import Device, DataType


device_specs = [
    {
        "uuid": "a4c56381-0f12-4227-9927-b9dea3563bad",
        "name": "Simple sensor 1",
        "description": "Some description",
        "category": Device.Category.SENSOR,
        "type": Device.Type.THERMOMETER,
        "data_sources": [
            {
                "name": "Temperature",
                "data_type": DataType.INT
            }
        ]
    },
    {
        "uuid": "45e6ac3f-9f84-44bf-9627-61d0fab9b3c6",
        "name": "Simple sensor 2",
        "description": "Some description",
        "category": Device.Category.SENSOR,
        "type": Device.Type.THERMOMETER,
        "data_sources": [
            {
                "name": "Temperature",
                "data_type": DataType.INT
            }
        ]
    },
    {
        "uuid": "08cc66dd-2b32-4ad8-97ff-84c2fc41ba7b",
        "name": "Simple sensor 3",
        "description": "Some description",
        "category": Device.Category.SENSOR,
        "type": Device.Type.THERMOMETER,
        "data_sources": [
            {
                "name": "Temperature",
                "data_type": DataType.INT
            }
        ]
    },
    {
        "uuid": "051f8c4b-001f-4fda-be35-9faee8a83496",
        "name": "Simple sensor 4",
        "description": "Some description",
        "category": Device.Category.SENSOR,
        "type": Device.Type.THERMOMETER,
        "data_sources": [
            {
                "name": "Temperature",
                "data_type": DataType.INT
            }
        ]
    },
    {
        "uuid": "4653be04-f030-44dd-a69d-af582db1ec5f",
        "name": "Simple sensor 5",
        "description": "Some description",
        "category": Device.Category.SENSOR,
        "type": Device.Type.THERMOMETER,
        "data_sources": [
            {
                "name": "Temperature",
                "data_type": DataType.INT
            }
        ]
    },
    {
        "uuid": "6c93d175-87cf-4963-bd88-16af4e4f7962",
        "name": "Simple sensor 6",
        "description": "Some description",
        "category": Device.Category.SENSOR,
        "type": Device.Type.THERMOMETER,
        "data_sources": [
            {
                "name": "Temperature",
                "data_type": DataType.INT
            }
        ]
    },
    {
        "uuid": "27667177-d8c2-4506-8ea0-629289dd4544",
        "name": "Simple sensor 7",
        "description": "Some description",
        "category": Device.Category.SENSOR,
        "type": Device.Type.THERMOMETER,
        "data_sources": [
            {
                "name": "Temperature",
                "data_type": DataType.INT
            }
        ]
    },
]
