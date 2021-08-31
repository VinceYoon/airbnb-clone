from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from . import models, forms


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


class RoomDetail(DetailView):
    """Room Detail View"""

    model = models.Room


class RoomSearch(View):
    """Room Search View"""

    def get(self, request):
        country = request.GET.get("country")
        form = forms.SearchForm(request.GET)
        context = {}

        if country and form.is_valid():
            params = form.cleaned_data

            filter_args = {}
            filter_args["country"] = params["country"]

            if params["city"] != "Anywhere":
                filter_args["city__startswith"] = params["city"]

            if params["room_type"] is not None:
                filter_args["room_type"] = params["room_type"]

            if params["price"] is not None:
                filter_args["price__lte"] = params["price"]

            if params["guests"] is not None:
                filter_args["guests__lte"] = params["guests"]

            if params["bedrooms"] is not None:
                filter_args["bedrooms__lte"] = params["bedrooms"]

            if params["beds"] is not None:
                filter_args["beds__lte"] = params["beds"]

            if params["baths"] is not None:
                filter_args["baths__lte"] = params["baths"]

            if params["instant_book"] is True:
                filter_args["instant_book"] = params["instant_book"]

            if params["superhost"] is True:
                filter_args["host__superhost"] = params["superhost"]

            for amenity in params["amenities"]:
                filter_args["amenities"] = amenity

            for facility in params["facilities"]:
                filter_args["facilities"] = facility

            query_set = models.Room.objects.filter(**filter_args).order_by("-created")
            paginator = Paginator(query_set, 10, orphans=5)
            page = request.GET.get("page", 1)
            rooms = paginator.get_page(page)

            context["form"] = form
            context["rooms"] = rooms
        else:
            empty_form = forms.SearchForm()
            context["form"] = empty_form

        return render(request, "rooms/sarch.html", context)
