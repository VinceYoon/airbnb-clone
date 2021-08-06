from django.db import models
from core import models as core_models


class Status(core_models.AbstractItem):
    """Status Model"""

    class Meta:
        verbose_name_plural = "Statuses"


class Reservation(core_models.TimeStampedModel):
    """Review Model"""

    check_in = models.DateField()
    check_out = models.DateField()

    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        "Status", related_name="reservations", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"
