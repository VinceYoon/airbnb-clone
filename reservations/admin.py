from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "is_progress",
        "is_finished",
    )

    list_filter = ("status",)
