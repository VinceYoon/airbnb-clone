from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.TimeStampedModel):
    """Review Model"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, STATUS_PENDING.capitalize()),
        (STATUS_CONFIRMED, STATUS_CONFIRMED.capitalize()),
        (STATUS_CANCELED, STATUS_CANCELED.capitalize()),
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()

    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def is_confirmed(self):
        return self.status == self.STATUS_CONFIRMED

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    def already_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    def is_progress(self):
        return self.is_confirmed() and self.in_progress()

    is_progress.boolean = True

    def is_finished(self):
        return self.is_confirmed() and self.already_finished()

    is_finished.boolean = True
