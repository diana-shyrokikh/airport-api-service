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


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country"]
    list_filter = ["country"]


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "closest_big_city"]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ["id", "source", "destination"]


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "airplane_type",
        "name",
        "rows",
        "seats_in_row"
    ]


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name"]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "route",
        "airplane",
        "departure_time",
        "arrival_time"
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "user"
    ]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "row",
        "seat",
        "order",
        "flight"
    ]
