from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    """List Admin"""

    list_display = (
        "name",
        "user",
    )

    search_fields = ("name",)
    filter_horizontal = ("rooms",)
