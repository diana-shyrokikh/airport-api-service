from django.urls import include, path
from rest_framework.routers import DefaultRouter

from airport.views import (
    CountryView,
    CityView,
    AirportView,
    RouteView,
    AirplaneTypeView,
    AirplaneView,
    CrewView,
    FlightView,
    OrderView,
    TicketView,
)

router = DefaultRouter()

router.register("countries", CountryView)
router.register("cities", CityView)
router.register("airports", AirportView)
router.register("routs", RouteView)
router.register("airplane_types", AirplaneTypeView)
router.register("airplanes", AirplaneView)
router.register("crew", CrewView)
router.register("flights", FlightView)
router.register("orders", OrderView)
router.register("tickets", TicketView)


urlpatterns = [
    path("", include(router.urls))
]

app_name = "airport"
