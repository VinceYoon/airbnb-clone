from django.views.generic import ListView
from django.shortcuts import redirect
from . import models


class HomeView(ListView):
    """HomeView"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"
    allow_empty = True

    def dispatch(self, *args, **kwargs):
        try:
            response = super(HomeView, self).dispatch(*args, **kwargs)
            response.render()
        except Exception:
            return redirect("/")
        return response
