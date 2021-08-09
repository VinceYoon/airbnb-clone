from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


class RoomType(core_models.AbstractItem):
    """Room Type Model"""

    class Meta:
        verbose_name = "Room Type"


class Amenity(core_models.AbstractItem):
    """Amenity Model"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(core_models.AbstractItem):
    """Facility Model"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(core_models.AbstractItem):
    """House Rule Model"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):
    """Photo Model"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):
    """Room Model"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=140)
    price = models.IntegerField()
    guests = models.IntegerField(help_text="how many people will be staying?")
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )

    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.title(self.city)
        super().save(*args, **kwargs)

    def total_rating(self):
        reviews = self.reviews.all()
        total = 0
        if len(reviews) > 0:
            for review in reviews:
                total += review.rating_average()
            return round(total / len(reviews), 2)
        return 0
