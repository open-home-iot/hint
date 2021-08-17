import uuid

from django.core.management.base import BaseCommand
from django.core.management import call_command

from backend.user.models import User
from backend.hume.models import ValidHume


class Command(BaseCommand):
    help = 'Generates data for live use'

    def handle(self, *args, **options):
        """
        Handle the command.
        """
        # Clear DB before generating test data
        call_command("flush")

        self.stdout.write("Starting data generation...")
        self.create_live_data()

    def create_live_data(self):
        """
        Create data needed for live use. Sets up:
          1. An admin account: admin@admin.se/password
          2. A dummy account: test@test.se/password
          3. A single ValidHume, who's ID is printed after creation
        """
        user = User.objects.create_user(email="t@t.se", password="password")
        self.stdout.write(f"Created user '{user.email}'")
        superuser = User.objects.create_superuser(email="admin@admin.se",
                                                  password="password")
        self.stdout.write(f"Created superuser '{superuser.email}'")

        # ValidHume
        unpaired_valid_hume = ValidHume.objects.create(uuid=uuid.uuid4())
        unpaired_hume_uuid = str(unpaired_valid_hume.uuid)
        self.stdout.write(f"ValidHume: "
                          f"{self.style.SUCCESS(unpaired_hume_uuid)}")
