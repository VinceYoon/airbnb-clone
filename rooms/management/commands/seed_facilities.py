from django.core.management.base import BaseCommand
from rooms.models import Facility

NAME = "facilities"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("seeding data..."))
        run_seed()
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} {NAME} created!"))


def run_seed():
    clear_data()
    for facility in facilities:
        Facility.objects.create(name=facility)


def clear_data():
    Facility.objects.all().delete()


facilities = [
    "Private entrance",
    "Paid parking on premises",
    "Paid parking off premises",
    "Elevator",
    "Parking",
    "Gym",
]
