import random
import zipfile
from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile
from django.contrib.admin.utils import flatten
from django.conf import settings
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


NAME = "rooms"


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
            run_seed_room(number)
            self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
        except Exception as error:
            self.stdout.write(self.style.ERROR("Error:" + repr(error)))


def run_seed_room(number):
    room_images = get_seed_room_img_list()
    seeder = Seed.seeder()
    all_users = user_models.User.objects.all()
    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()
    house_rules = room_models.HouseRule.objects.all()

    seeder.add_entity(
        room_models.Room,
        number,
        {
            "name": lambda x: seeder.faker.address(),
            "host": lambda x: random.choice(all_users),
            "room_type": lambda x: random.choice(room_types),
            "guests": lambda x: random.randint(1, 5),
            "price": lambda x: random.randint(1, 300),
            "bedrooms": lambda x: random.randint(1, 5),
            "beds": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),
        },
    )
    rooms = seeder.execute()
    room_ids = flatten(list(rooms.values()))
    for room_id in room_ids:
        room = room_models.Room.objects.get(pk=room_id)
        for i in range(random.randint(4, 6)):
            room_models.Photo.objects.create(
                caption=seeder.faker.sentence(),
                room=room,
                file=random.choice(room_images),
            )

        for amenity in amenities:
            magic_number = random.randint(0, 15)
            if magic_number % 2 == 0:
                room.amenities.add(amenity)

        for facility in facilities:
            magic_number = random.randint(0, 15)
            if magic_number % 2 == 0:
                room.facilities.add(facility)

        for house_rule in house_rules:
            magic_number = random.randint(0, 15)
            if magic_number % 2 == 0:
                room.house_rules.add(house_rule)


def get_seed_room_img_list():
    seed_room_image_zip_path = str(settings.BASE_DIR) + "/seed_room_images.zip"
    img_zip = zipfile.ZipFile(seed_room_image_zip_path)
    org_info_list = img_zip.infolist()
    room_img_list = []
    for info in org_info_list:
        if not str(info.filename).startswith("__MACOSX/"):
            file = img_zip.open(info)
            img = DjangoFile(file)
            room_img_list.append(img)

    return room_img_list
