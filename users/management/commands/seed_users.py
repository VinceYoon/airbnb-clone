import random
import zipfile
from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile
from django.conf import settings
from django_seed import Seed
from users.models import User


NAME = "users"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="Number of {NAME} to create"
        )
        parser.add_argument("--type", type=str, help="User Type")

    def handle(self, *arg, **options):
        type = options["type"]
        number = options["number"]

        if type == "admin":
            self.stdout.write(self.style.NOTICE("seeding data..."))
            try:
                run_seed_admin(number)
                self.stdout.write(self.style.SUCCESS("admin user created!"))
            except Exception as error:
                self.stdout.write(self.style.ERROR("Error:" + repr(error)))
        else:
            try:
                run_seed_users(number)
                self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
            except Exception as error:
                self.stdout.write(self.style.ERROR("Error:" + repr(error)))


def run_seed_admin(number):
    if number > 1:
        raise ValueError("Only one admin can be created.")
    else:
        User.objects.create_superuser("admin", "admin.test.com", "12345")


def run_seed_users(number):
    avatar_images = get_seed_avatar_img_list()
    if number > 20:
        raise ValueError("Max creation is 20")
    else:
        seeder = Seed.seeder()
        seeder.add_entity(
            User,
            number,
            {
                "is_staff": False,
                "is_superuser": False,
                "avatar": lambda x: random.choice(avatar_images),
            },
        )
        seeder.execute()


def get_seed_avatar_img_list():
    seed_avatar_image_zip_path = str(settings.BASE_DIR) + "/seed_avatar_images.zip"
    img_zip = zipfile.ZipFile(seed_avatar_image_zip_path)
    org_info_list = img_zip.infolist()
    avatar_img_list = []
    for info in org_info_list:
        if not str(info.filename).startswith("__MACOSX/"):
            file = img_zip.open(info)
            img = DjangoFile(file)
            avatar_img_list.append(img)

    return avatar_img_list
