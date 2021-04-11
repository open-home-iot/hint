import uuid

from django.core.management.base import BaseCommand
from django.core.management import call_command

from backend.user.models import User
from backend.home.models import Home, Room
from backend.hume.models import ValidHume, Hume
from backend.device.models import Device, create_device

from backend.core.management.commands.devices import device_specs


class Command(BaseCommand):
    help = 'Generates data for testing'

    def handle(self, *args, **options):
        """
        Handle the command.
        """
        # Clear DB before generating test data
        self.stdout.write("Flushing DB...")
        call_command("flush")

        self.stdout.write("Starting test data generation...")
        Command.create_test_data()

    @staticmethod
    def create_test_data():
        """
        Create the test data.
        """
        user = User.objects.create_user(email="t@t.se", password="password")
        User.objects.create_superuser(email="admin@admin.se",
                                      password="password")

        # Create some homes
        for home_name in ["House", "Apartment"]:
            home = Home.objects.create(name=home_name)
            home.users.add(user)

        [home1, home2] = Home.objects.all()

        # Create some rooms for home1
        for room_name in ["Livingroom", "Bedroom", "Attic", "Basement"]:
            Room.objects.create(name=room_name, home=home1)

        # Create some rooms for home2
        for room_name in ["Livingroom", "Bedroom", "Hallway"]:
            Room.objects.create(name=room_name, home=home2)

        # Humes for home1
        for _ in range(2):
            hume_uuid = uuid.uuid4()
            ValidHume.objects.create(uuid=hume_uuid)
            User.objects.create_hume_user(hume_uuid, str(uuid.uuid4()))
            Hume.objects.create(uuid=hume_uuid, home=home1)

        # One more ValidHume for testing pairing procedure
        ValidHume.objects.create(uuid=uuid.uuid4())

        # Hume for home2
        hume_uuid = uuid.uuid4()
        ValidHume.objects.create(uuid=hume_uuid)
        User.objects.create_hume_user(hume_uuid, str(uuid.uuid4()))
        Hume.objects.create(uuid=hume_uuid, home=home2)

        # Create some devices for each Hume
        humes = Hume.objects.all()
        hume_index = 0
        for device_spec in device_specs:
            create_device(humes[hume_index], device_spec)

            hume_index += 1
            if hume_index == len(humes):
                hume_index = 0

        # Assign the devices to a room
        def assign_home_devices_to_rooms(home):
            """
            Get all devices of the home and assign them to rooms of the home.
            """
            home_rooms = Room.objects.filter(home=home)
            room_index = 0
            for device in Device.objects.filter(hume__home=home):
                device.room = home_rooms[room_index]
                device.save()

                room_index += 1
                if room_index == len(home_rooms):
                    room_index = 0

        assign_home_devices_to_rooms(home1)
        assign_home_devices_to_rooms(home2)
