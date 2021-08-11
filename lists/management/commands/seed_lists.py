import random
from django.core.management.base import BaseCommand
from lists.models import List as WishList
from users import models as user_models
from rooms import models as room_models


NAME = "wishlists"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def handle(self, *arg, **options):
        try:
            run_seed_lists()
            self.stdout.write(self.style.SUCCESS(f"created {NAME} for all users!"))
        except Exception as error:
            self.stdout.write(self.style.ERROR("Error:" + repr(error)))


def clear_data():
    WishList.objects.all().delete()


def run_seed_lists():
    clear_data()
    users = user_models.User.objects.all().exclude(is_superuser=True)
    rooms = room_models.Room.objects.all()

    for user in users:
        list_model = WishList.objects.create(user=user, name=f"Favs - {user.username}")
        rooms_for_adding = []
        random_limit = random.randint(1, 7)
        for room in rooms:
            if len(rooms_for_adding) > random_limit:
                break

            magic_number = random.randint(0, 15)
            if magic_number % 2 == 0:
                rooms_for_adding.append(room)

        list_model.rooms.add(*rooms_for_adding)
