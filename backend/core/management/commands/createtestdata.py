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
        call_command("flush")

        self.stdout.write("Starting test data generation...")
        self.create_test_data()

    def create_test_data(self):
        """
        Create the test data.
        """
        user = User.objects.create_user(email="t@t.se", password="password")
        self.stdout.write(f"Created user '{user.email}'")
        superuser = User.objects.create_superuser(email="admin@admin.se",
                                                  password="password")
        self.stdout.write(f"Created superuser '{superuser.email}'")

        # Create some homes
        for home_name in ["House", "Apartment"]:
            home = Home.objects.create(name=home_name)
            home.users.add(user)
            self.stdout.write(f"Created home '{home.name}' "
                              f"for user '{user.email}'")

        [home1, home2] = Home.objects.all()

        # Create some rooms for home1
        for room_name in ["Livingroom", "Bedroom", "Attic", "Basement"]:
            Room.objects.create(name=room_name, home=home1)
            self.stdout.write(f"Added room '{room_name}' "
                              f"to home '{home1.name}'")

        # Create some rooms for home2
        for room_name in ["Livingroom", "Bedroom", "Hallway"]:
            Room.objects.create(name=room_name, home=home2)
            self.stdout.write(f"Added room '{room_name}' "
                              f"to home '{home2.name}'")

        # Humes for home1
        for _ in range(2):
            hume_uuid = uuid.uuid4()
            ValidHume.objects.create(uuid=hume_uuid)
            User.objects.create_hume_user(hume_uuid, str(uuid.uuid4()))
            Hume.objects.create(uuid=hume_uuid, home=home1)
            self.stdout.write(f"Created hume '{hume_uuid}' "
                              f"for home '{home1.name}'")

        # One more ValidHume for testing pairing procedure
        unpaired_valid_hume = ValidHume.objects.create(uuid=uuid.uuid4())
        unpaired_hume_uuid = str(unpaired_valid_hume.uuid)

        # Hume for home2
        hume_uuid = uuid.uuid4()
        ValidHume.objects.create(uuid=hume_uuid)
        User.objects.create_hume_user(hume_uuid, str(uuid.uuid4()))
        Hume.objects.create(uuid=hume_uuid, home=home2)
        self.stdout.write(f"Created hume '{hume_uuid}' "
                          f"for home '{home2.name}'")

        # Create some devices for each Hume
        humes = Hume.objects.all()
        hume_index = 0
        for device_spec in device_specs:
            create_device(humes[hume_index], device_spec)
            self.stdout.write(f"Added device '{device_spec['uuid']}' "
                              f"to hume '{str(humes[hume_index].uuid)}'")

            hume_index += 1
            if hume_index == len(humes):
                hume_index = 0

        # Assign the devices to a room
        def assign_home_devices_to_rooms(stdout, home):
            """
            Get all devices of the home and assign them to rooms of the home.
            """
            stdout.write(f"Assigning devices of home '{home.name}' to "
                         f"rooms...")

            home_rooms = Room.objects.filter(home=home)
            room_index = 0
            for device in Device.objects.filter(hume__home=home):
                device.room = home_rooms[room_index]
                device.save()
                stdout.write(f"Assigned device {device.uuid} "
                             f"to room '{home_rooms[room_index].name}'")

                room_index += 1
                if room_index == len(home_rooms):
                    room_index = 0

        assign_home_devices_to_rooms(self.stdout, home1)
        assign_home_devices_to_rooms(self.stdout, home2)

        self.stdout.write(f"Vacant HUME: "
                          f"{self.style.SUCCESS(unpaired_hume_uuid)}")
