from django.core.management.base import BaseCommand

from backend.user.models import User


class Command(BaseCommand):
    """
    Use this command the FIRST TIME HINT is deployed to have a superuser to
    go from. Make sure to change the password IMMEDIATELY after creation.
    """
    help = 'Generates a single superuser as long as NO OTHER users exist'

    def handle(self, *args, **options):
        self.stdout.write("Checking if data generation is permitted...")
        users = User.objects.all()
        if users.exists():
            self.stderr.write("Users already exist, exiting...")
            return

        self.stdout.write("Starting data generation...")
        superuser = User.objects.create_superuser(email="admin@admin.se",
                                                  password="password")
        self.stdout.write(f"Created superuser '{superuser.email}'")
