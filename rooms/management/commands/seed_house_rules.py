from django.core.management.base import BaseCommand
from rooms.models import HouseRule

NAME = "house_rules"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("seeding data..."))
        run_seed()
        self.stdout.write(self.style.SUCCESS(f"{len(house_rules)} {NAME} created!"))


def run_seed():
    clear_data()
    for house_rule in house_rules:
        HouseRule.objects.create(name=house_rule)


def clear_data():
    HouseRule.objects.all().delete()


house_rules = [
    "Pet Allowed",
    "Smoking Allowed",
]
