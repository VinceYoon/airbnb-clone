from django.core.management.base import BaseCommand
from rooms.models import RoomType

NAME = "room_types"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("seeding data..."))
        run_seed()
        self.stdout.write(self.style.SUCCESS(f"{len(room_types)} {NAME} created!"))


def run_seed():
    clear_data()
    for room_type in room_types:
        RoomType.objects.create(name=room_type)


def clear_data():
    RoomType.objects.all().delete()


room_types = [
    "Entire Place",
    "Private Room",
    "Hotel Room",
    "Shared Room",
]
