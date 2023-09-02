from django.contrib import admin

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country"]
    list_filter = ["country"]
    search_fields = ["name"]


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "closest_big_city"]
    search_fields = ["name"]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "source",
        "destination",
        "distance"
    ]
    search_fields = [
        "source__closest_big_city__name",
        "destination__closest_big_city__name"
    ]


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "airplane_type",
        "name",
        "rows",
        "seats_in_row"
    ]
    search_fields = ["name"]
    list_filter = ["airplane_type"]


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "route",
        "airplane",
        "departure_time",
        "arrival_time"
    ]
    search_fields = [
        "route__source__closest_big_city__name",
        "route__destination__closest_big_city__name"
    ]


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)
    list_display = [
        "id",
        "created_at",
        "user"
    ]
    search_fields = ["user"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "row",
        "seat",
        "order",
        "flight"
    ]
    search_fields = [
        "flight__route__source__closest_big_city__name",
        "flight__route__destination__closest_big_city__name",
    ]
