from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from airport.get_ids import get_ids
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
from airport.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
    FlightSerializer,
    OrderSerializer,
    TicketSerializer,
    CityListSerializer,
    CityDetailSerializer,
    AirportDetailSerializer,
    AirportListSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    CrewListSerializer,
    CrewDetailSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    AirplaneTypeListSerializer,
    AirplaneTypeDetailSerializer,
    CountryListSerializer,
    CountryDetailSerializer,
)


class TwoSizePagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page_size"
    max_page_size = 100


class FiveSizePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class TenSizePagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page_size"
    max_page_size = 100


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = FiveSizePagination

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")

        if self.action != "destroy":
            queryset = Country.objects.prefetch_related("cities")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = CountryListSerializer
        elif self.action == "retrieve":
            serializer_class = CountryDetailSerializer

        return serializer_class


class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = FiveSizePagination

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        country_ids = self.request.query_params.get("country")

        if self.action != "destroy":
            queryset = City.objects.select_related("country")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if country_ids:
            country_ids = get_ids(country_ids)
            queryset = queryset.filter(country__in=country_ids)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = CityListSerializer
        elif self.action == "retrieve":
            serializer_class = CityDetailSerializer

        return serializer_class


class AirportView(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = FiveSizePagination

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        country_ids = self.request.query_params.get("country")
        city_ids = self.request.query_params.get("city")

        if self.action != "destroy":
            queryset = Airport.objects.select_related("closest_big_city__country")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if country_ids:
            country_ids = get_ids(country_ids)
            queryset = queryset.filter(country__in=country_ids)

        if city_ids:
            city_ids = get_ids(city_ids)
            queryset = queryset.filter(closest_big_city__in=city_ids)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = AirportListSerializer
        elif self.action == "retrieve":
            serializer_class = AirportDetailSerializer

        return serializer_class


class RouteView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    pagination_class = FiveSizePagination

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "destroy":
            queryset = Route.objects.select_related(
                "source__closest_big_city__country",
                "destination__closest_big_city__country",
            )

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = RouteListSerializer
        elif self.action == "retrieve":
            serializer_class = RouteDetailSerializer

        return serializer_class


class AirplaneTypeView(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = FiveSizePagination

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "destroy":
            queryset = AirplaneType.objects.prefetch_related("airplanes",)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = AirplaneTypeListSerializer
        elif self.action == "retrieve":
            serializer_class = AirplaneTypeDetailSerializer

        return serializer_class


class AirplaneView(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    pagination_class = FiveSizePagination

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "destroy":
            queryset = Airplane.objects.select_related("airplane_type",)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = AirplaneListSerializer
        elif self.action == "retrieve":
            serializer_class = AirplaneDetailSerializer

        return serializer_class


class CrewView(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = TenSizePagination

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "destroy":
            queryset = Crew.objects.prefetch_related("flights",)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = CrewListSerializer
        elif self.action == "retrieve":
            serializer_class = CrewDetailSerializer

        return serializer_class


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    pagination_class = TwoSizePagination

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "destroy":
            queryset = Flight.objects.prefetch_related("crew").select_related(
                "route__destination__closest_big_city__country",
                "route__source__closest_big_city__country",
                "airplane__airplane_type")

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = FlightListSerializer
        elif self.action == "retrieve":
            serializer_class = FlightDetailSerializer

        return serializer_class


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = TwoSizePagination

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = OrderListSerializer
        elif self.action == "retrieve":
            serializer_class = OrderDetailSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "destroy":
            queryset = Order.objects.prefetch_related(
                "tickets__flight__route__destination__closest_big_city__country",
                "tickets__flight__route__source__closest_big_city__country",
                "tickets__flight__airplane__airplane_type"
            )

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = FiveSizePagination

    def get_queryset(self):
        queryset = self.queryset

        if self.action != "destroy":
            queryset = Ticket.objects.select_related(
                "order",
                "flight__route__destination__closest_big_city__country",
                "flight__route__source__closest_big_city__country",
                "flight__airplane__airplane_type"
            )

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = TicketListSerializer
        elif self.action == "retrieve":
            serializer_class = TicketDetailSerializer

        return serializer_class
