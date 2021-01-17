from abc import ABC

from django.db import models

from backend.hume.models import Hume


class _Choices(ABC):

    # Subclasses shall override
    CHOICES = []

    @classmethod
    def get_verbose_name(cls, key):
        """
        Utility to fetch verbose category names.

        :param key: choice key
        :return: verbose choice string
        """
        for choice in cls.CHOICES:
            if choice[0] == key:
                return choice[1]


class DataType(_Choices):
    STR = 0
    INT = 1
    FLOAT = 2
    BOOL = 3
    PERC_INT = 4
    PERC_FLOAT = 5

    CHOICES = [
        (STR, "String"),
        (INT, "Integer"),
        (FLOAT, "Float"),
        (BOOL, "Boolean"),
        (PERC_INT, "% Integer"),
        (PERC_FLOAT, "% Float")
    ]


def create_device(hume, device_spec):
    """
    Creates all objects necessary from the device specification: Device,
    DeviceAction (if present), DeviceDataSource (if present).

    :param hume: HUME the device belongs to, this shall always be present when
                 creating a new device, as it will be created as a result of
                 a discovery and attach procedure
    :type hume: Hume
    :param device_spec: as received from HUME
    :type device_spec: dict
    """
    device_dict = {
        "hume": hume,
        "uuid": device_spec["uuid"],
        "name": device_spec["name"],
        "category": device_spec["category"],
        "type": device_spec["type"]
    }

    if device_spec.get("description") is not None:
        device_dict["description"] = device_spec["description"]

    device = Device.objects.create(**device_dict)

    data_sources = {}
    if device_spec.get("data_sources") is not None:
        for data_source_spec in device_spec["data_sources"]:
            data_source = DeviceDataSource.objects.create(
                device=device,
                data_source_id=data_source_spec["id"],
                name=data_source_spec["name"],
                data_type=data_source_spec["data_type"]
            )
            data_sources[data_source.data_source_id] = data_source

    for action in device_spec["actions"]:
        # MUST fields
        device_action = {
            "device": device,
            "action_id": action["id"],
            "name": action["name"],
            "type": action["type"],
        }

        # OPTIONAL fields
        if action.get("description") is not None:
            device_action["description"] = action["description"]
        if action.get("data_source") is not None:
            device_action["data_source"] = \
                data_sources[action["data_source"]]

        DeviceAction.objects.create(**device_action)


class Device(models.Model):
    hume = models.ForeignKey(Hume, on_delete=models.CASCADE)
    is_attached = models.BooleanField(default=False)

    # Device specification
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=258, null=True, blank=True)

    class Category(_Choices):
        SENSOR = 0
        ACTUATOR = 1
        COLLECTION = 2

        CHOICES = [
            (SENSOR, "Sensor"),
            (ACTUATOR, "Actuator"),
            (COLLECTION, "Collection"),
        ]

    category = models.IntegerField(choices=Category.CHOICES)

    class Type(_Choices):
        THERMOMETER = 0
        CUSTOM = 666

        CHOICES = [
            (THERMOMETER, "Thermometer"),
            (CUSTOM, "Custom")
        ]

    def get_type_name(self, device_type):
        """
        Since custom device types are possible, fetch the custom_type_name if
        type is CUSTOM, otherwise default to get_verbose_name from _Choices.

        :param device_type: integer representation of a device type
        :return: verbose type name
        """
        if device_type == self.Type.CUSTOM:
            return self.custom_type_name

        return self.Type.get_verbose_name(device_type)

    type = models.IntegerField(choices=Type.CHOICES)
    custom_type_name = models.CharField(max_length=25, null=True, blank=True)

    # When deleting parent, cascade to children
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        """str representation of a Device instance"""
        return f"<{self.__class__.__name__} instance {self.uuid} (" \
               f"hume owner: {self.hume.uuid}, is_attached: {self.is_attached}" \
               f", name: {self.name}, category: " \
               f"{Device.Category.get_verbose_name(self.category)}" \
               f", type: {self.get_type_name(self.type)}, " \
               f"parent: {self.parent})>"


class DeviceDataSource(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    data_source_id = models.IntegerField()
    name = models.CharField(max_length=50)
    data_type = models.IntegerField(choices=DataType.CHOICES)

    class Meta:
        unique_together = [['device', 'data_source_id']]

    def __str__(self):
        """str representation of a DeviceDataSource instance"""
        return f"<{self.__class__.__name__} instance {self.id} (related " \
               f"device: {self.device.uuid}, data_source_id: " \
               f"{self.data_source_id}, name: {self.name}, data_type: " \
               f"{DataType.get_verbose_name(self.data_type)})>"


class DeviceAction(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    action_id = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=258, null=True, blank=True)

    class Type(_Choices):
        VANILLA = 0
        READ = 1
        STATEFUL = 2
        PARAMETERIZED = 3

        CHOICES = [
            (VANILLA, "Vanilla"),
            (READ, "Read"),
            (STATEFUL, "Stateful"),
            (PARAMETERIZED, "Parameterized"),
        ]

    type = models.IntegerField(choices=Type.CHOICES)

    # For READ actions only
    data_source = models.ForeignKey(DeviceDataSource,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)

    class Meta:
        # Ensure a device has uniquely identifiable actions
        unique_together = [['device', 'action_id']]

    def __str__(self):
        """str representation of a DeviceAction instance"""
        return f"<{self.__class__.__name__} instance {self.id} (related " \
               f"device: {self.device.uuid}, action_id: {self.action_id}, " \
               f"name: {self.name}, type: " \
               f"{DeviceAction.Type.get_verbose_name(self.type)}, " \
               f"data_source: {self.data_source.id})>"


class DeviceReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    data_source = models.ForeignKey(DeviceDataSource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    data = models.CharField(max_length=25)

    def __str__(self):
        """str representation of a DeviceReading instance"""
        return f"<{self.__class__.__name__} instance {self.id} (related " \
               f"device: {self.device.uuid}, data_source: " \
               f"{self.data_source.id}, timestamp: {self.timestamp}, data: " \
               f"{self.data})>"
