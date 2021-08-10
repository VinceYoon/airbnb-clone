from django.core.management.base import BaseCommand
from rooms.models import Amenity

NAME = "amenities"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("seeding data..."))
        run_seed()
        self.stdout.write(self.style.SUCCESS(f"{len(amenities)} {NAME} created!"))


def run_seed():
    clear_data()
    for amenity in amenities:
        Amenity.objects.create(name=amenity)


def clear_data():
    Amenity.objects.all().delete()


amenities = [
    "Air conditioning",
    "Alarm Clock",
    "Balcony",
    "Bathroom",
    "Bathtub",
    "Bed Linen",
    "Boating",
    "Cable TV",
    "Carbon monoxide detectors",
    "Chairs",
    "Children Area",
    "Coffee Maker in Room",
    "Cooking hob",
    "Cookware & Kitchen Utensils",
    "Dishwasher",
    "Double bed",
    "En suite bathroom",
    "Free Parking",
    "Free Wireless Internet",
    "Freezer",
    "Fridge / Freezer",
    "Golf",
    "Hair Dryer",
    "Heating",
    "Hot tub",
    "Indoor Pool",
    "Ironing Board",
    "Microwave",
    "Outdoor Pool",
    "Outdoor Tennis",
    "Oven",
    "Queen size bed",
    "Restaurant",
    "Shopping Mall",
    "Shower",
    "Smoke detectors",
    "Sofa",
    "Stereo",
    "Swimming pool",
    "Toilet",
    "Towels",
    "TV",
]
