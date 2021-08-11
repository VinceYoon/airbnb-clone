import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations.models import Reservation
from users import models as user_models
from rooms import models as room_models


NAME = "reservations"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="Number of {NAME} to create"
        )

    def handle(self, *arg, **options):
        number = options["number"]
        self.stdout.write(self.style.NOTICE("seeding data..."))
        try:
            run_seed_reservations(number)
            self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
        except Exception as error:
            self.stdout.write(self.style.ERROR("Error:" + repr(error)))


def clear_data():
    Reservation.objects.all().delete()


def run_seed_reservations(number):
    clear_data()
    seeder = Seed.seeder()
    users = user_models.User.objects.all().exclude(is_superuser=True)
    rooms = room_models.Room.objects.all()
    seeder.add_entity(
        Reservation,
        number,
        {
            "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
            "guest": lambda x: random.choice(users),
            "room": lambda x: random.choice(rooms),
            "check_in": lambda x: datetime.now() - timedelta(days=random.randint(0, 5)),
            "check_out": lambda x: datetime.now()
            + timedelta(days=random.randint(0, 5)),
        },
    )
    seeder.execute()
