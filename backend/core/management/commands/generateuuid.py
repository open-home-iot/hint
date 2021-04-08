import uuid

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generates a UUID'

    def add_arguments(self, parser):
        parser.add_argument("no_uuids", type=int)

    def handle(self, *args, **options):
        """
        Handle the command.
        """
        for _ in range(options["no_uuids"]):
            self.stdout.write(self.style.SUCCESS(uuid.uuid4()))
