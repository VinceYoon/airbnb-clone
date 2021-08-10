import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews.models import Review
from users import models as user_models
from rooms import models as room_models


NAME = "reviews"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="Number of {NAME} to create"
        )

    def handle(self, *arg, **options):
        number = options["number"]
        try:
            run_seed_reviews(number)
            self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
        except Exception as error:
            self.stdout.write(self.style.ERROR("Error:" + repr(error)))


def run_seed_reviews(number):
    seeder = Seed.seeder()
    users = user_models.User.objects.all()
    rooms = room_models.Room.objects.all()
    seeder.add_entity(
        Review,
        number,
        {
            "accuracy": lambda x: random.randint(0, 5),
            "communication": lambda x: random.randint(0, 5),
            "cleanliness": lambda x: random.randint(0, 5),
            "location": lambda x: random.randint(0, 5),
            "check_in": lambda x: random.randint(0, 5),
            "value": lambda x: random.randint(0, 5),
            "room": lambda x: random.choice(rooms),
            "user": lambda x: random.choice(users),
        },
    )
    seeder.execute()
