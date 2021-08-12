from abc import ABC

from django.db import models

from backend.hume.models import Hume
from backend.home.models import Room


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
    """
    Specifies data types a device can report it supports for a data source/
    action input.
    """

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
    DeviceDataSource (if present).

    EXAMPLE STATEFUL DEVICE SPEC:
    {
      'uuid': '0ededfd1-65aa-42ba-866e-fb5c5ad607f2',
      'category': 1,  # Device.Category.ACTUATOR
      'type': 1,      # Device.Type.LAMP
      'states': [
                  {
                    'id': 0,
                    'control': [{'on': 1}, {'off': 0}]
                  }
                ]
    }

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

    device = Device(**device_dict)

    # States, data sources, etc.
    other_objects = []

    if device_spec.get("states") is not None:
        for state_group in device_spec["states"]:
            device_state_group = DeviceStateGroup(
                device=device,
                group_id=state_group.pop("id"),
            )
            group_name = list(state_group.keys())[0]  # only group name left
            device_state_group.group_name = group_name
            other_objects.append(device_state_group)

            group_states = state_group[group_name]
            for state in group_states:
                device_state = DeviceState(
                    device_state_group=device_state_group,
                    state_id=list(state.values())[0],
                    state_name=list(state.keys())[0],
                )
                other_objects.append(device_state)

    device.save()
    for obj in other_objects:
        obj.save()


class Device(models.Model):

    hume = models.ForeignKey(Hume, on_delete=models.CASCADE)

    # When Rooms are deleted, do not delete devices, they belong to the general
    # Home now.
    room = models.ForeignKey(Room,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL)

    # Device specification
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=258, null=True, blank=True)

    class Category(_Choices):
        """
        Specifies the different device categories, it is an inner class to
        enhance code readability through the referencing format:
        Device.Category.SENSOR. It reads really well.
        """

        SENSOR = 0
        ACTUATOR = 1
        COLLECTION = 2

        CHOICES = [
            (SENSOR, "Sensor"),
            (ACTUATOR, "Actuator"),
            (COLLECTION, "Collection"),
        ]

    category = models.IntegerField(choices=Category.CHOICES)

    @property
    def category_name(self):
        """
        The verbose category name of the device.

        :return: verbose category name
        """
        return Device.Category.get_verbose_name(self.category)

    class Type(_Choices):
        """
        Device type, either custom or known. Custom devices have to report
        a custom_device_name. This is an inner class for the same reason as
        the device category.
        """

        THERMOMETER = 0
        LAMP = 1
        CUSTOM = 666

        CHOICES = [
            (THERMOMETER, "Thermometer"),
            (LAMP, "Lamp"),
            (CUSTOM, "Custom"),
        ]

    @property
    def type_name(self):
        """
        The verbose type name of the device.

        :return: verbose type name
        """
        if self.type == Device.Type.CUSTOM:
            return self.custom_type_name

        return Device.Type.get_verbose_name(self.type)

    type = models.IntegerField(choices=Type.CHOICES)
    custom_type_name = models.CharField(max_length=25, null=True, blank=True)

    # When deleting parent, cascade to children
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    @property
    def states(self):
        """
        Fetch any states that are associated with the device.

        :returns: [DeviceState]
        """
        return DeviceState.objects.select_related(
            'device_state_group'
        ).filter(device_state_group__device__uuid=self.uuid)

    def __str__(self):
        """str representation of a Device instance"""
        return f"<{self.__class__.__name__} instance {self.uuid} (" \
               f"hume owner: {self.hume.uuid}, " \
               f"name: {self.name}, " \
               f"category: {self.category_name}, " \
               f"type: {self.type_name}, " \
               f"parent: {self.parent})>"  # noqa


class DeviceStateGroup(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    group_id = models.IntegerField()
    group_name = models.CharField(max_length=20)


class DeviceState(models.Model):

    device_state_group = models.ForeignKey(
        DeviceStateGroup, on_delete=models.CASCADE)
    state_id = models.IntegerField()
    state_name = models.CharField(max_length=50)


class DeviceDataSource(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    data_type = models.IntegerField(choices=DataType.CHOICES)

    def __str__(self):
        """str representation of a DeviceDataSource instance"""
        return f"<{self.__class__.__name__} instance {self.id} (related " \
               f"device: {self.device.uuid}, name: {self.name}, data_type: " \
               f"{DataType.get_verbose_name(self.data_type)})>"


class DeviceReading(models.Model):

    data_source = models.ForeignKey(DeviceDataSource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    data = models.CharField(max_length=25)

    def __str__(self):
        """str representation of a DeviceReading instance"""
        return f"<{self.__class__.__name__} instance {self.id} (" \
               f"data_source: {self.data_source.id}, " \
               f"timestamp: {self.timestamp}, data: " \
               f"{self.data})>"
