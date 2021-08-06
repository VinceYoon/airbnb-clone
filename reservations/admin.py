from django.contrib import admin
from . import models


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    """Status Admin"""

    list_display = ("name",)


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
    )

    list_filter = ("status",)
