from django.db.models import F, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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
    TakenTicketsSerializer,
)

from airport.paginations import (
    TwoSizePagination,
    FiveSizePagination,
    TenSizePagination
)
from user.permissions import IsAdminOrIfAuthenticatedReadOnly


class CountryView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = FiveSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter by name (ex. ?name=name)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CityView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = FiveSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        country_ids = self.request.query_params.get("countries")

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter by name (ex. ?name=name)",
                required=False,
            ),
            OpenApiParameter(
                "countries",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by countries id (ex. ?countries=1,2)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirportView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = FiveSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        country_ids = self.request.query_params.get("countries")
        city_ids = self.request.query_params.get("cities")

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter by name (ex. ?name=name)",
                required=False,
            ),
            OpenApiParameter(
                "countries",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by countries id (ex. ?countries=1,2)",
                required=False,
            ),
            OpenApiParameter(
                "cities",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by cities id (ex. ?cities=3,4)",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    pagination_class = FiveSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if self.action != "destroy":
            queryset = Route.objects.select_related(
                "source__closest_big_city__country",
                "destination__closest_big_city__country",
            )

        if source:
            queryset = queryset.filter(source__name__icontains=source)

        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = RouteListSerializer
        elif self.action == "retrieve":
            serializer_class = RouteDetailSerializer

        return serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type=str,
                description="Filter by source (ex. ?source=name)",
                required=False,
            ),
            OpenApiParameter(
                "destination",
                type=str,
                description="Filter by destination (ex. ?destination=name)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirplaneTypeView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    pagination_class = FiveSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")

        if self.action != "destroy":
            queryset = AirplaneType.objects.prefetch_related("airplanes",).annotate(
                airplane_count=Count("airplanes")
            )

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = AirplaneTypeListSerializer
        elif self.action == "retrieve":
            serializer_class = AirplaneTypeDetailSerializer

        return serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter by name (ex. ?name=name)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirplaneView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    pagination_class = FiveSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        airplane_type = self.request.query_params.get("airplane_type")
        capacity = self.request.query_params.get("capacity")

        if self.action != "destroy":
            queryset = Airplane.objects.select_related("airplane_type",)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if airplane_type:
            queryset = queryset.filter(
                airplane_type__name__icontains=airplane_type
            )

        if capacity:
            queryset = queryset.annotate(
                capacity=F("rows") * F("seats_in_rows")
            ).filter(capacity=capacity)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = AirplaneListSerializer
        elif self.action == "retrieve":
            serializer_class = AirplaneDetailSerializer

        return serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=str,
                description="Filter by name (ex. ?name=name)",
                required=False,
            ),
            OpenApiParameter(
                "airplane type",
                type=str,
                description="Filter by airplane type (ex. ?airplane_type=name)",
                required=False,
            ),
            OpenApiParameter(
                "capacity",
                type=int,
                description="Filter by capacity (ex. ?capacity=500)",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CrewView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = TenSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if self.action != "destroy":
            queryset = Crew.objects.prefetch_related("flights",)

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = CrewListSerializer
        elif self.action == "retrieve":
            serializer_class = CrewDetailSerializer

        return serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first name",
                type=str,
                description="Filter by first name (ex. ?first_name=name)",
                required=False,
            ),
            OpenApiParameter(
                "last name",
                type=str,
                description="Filter by last name (ex. ?last_name=name)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FlightView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    pagination_class = TwoSizePagination
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        departure_date = self.request.query_params.get("departure_date")
        arrival_date = self.request.query_params.get("arrival_date")
        to_city = self.request.query_params.get("to")
        from_city = self.request.query_params.get("from")

        if self.action != "destroy":
            queryset = Flight.objects.prefetch_related("crew").select_related(
                "route__destination__closest_big_city__country",
                "route__source__closest_big_city__country",
                "airplane__airplane_type").annotate(
                tickets_available=(
                        F("airplane__rows")
                        * F("airplane__seats_in_rows")
                        - Count("tickets")
                )
            )

        if departure_date:
            queryset = queryset.filter(departure_time__date=departure_date)

        if arrival_date:
            queryset = queryset.filter(arrival_time__date=arrival_date)

        if to_city:
            queryset = queryset.filter(
                route__destination__closest_big_city_id=to_city
            )

        if from_city:
            queryset = queryset.filter(
                route__source__closest_big_city_id=from_city
            )

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = FlightListSerializer
        elif self.action == "retrieve":
            serializer_class = FlightDetailSerializer

        return serializer_class


class OrderView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = TwoSizePagination
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = OrderListSerializer
        elif self.action == "retrieve":
            serializer_class = OrderDetailSerializer

        return serializer_class

    def get_queryset(self):
        queryset = self.queryset

        created_at_date = self.request.query_params.get("date")

        if self.action != "destroy":
            queryset = Order.objects.prefetch_related(
                "tickets__flight__route__destination__closest_big_city__country",
                "tickets__flight__route__source__closest_big_city__country",
                "tickets__flight__airplane__airplane_type"
            )

        if created_at_date:
            queryset = queryset.filter(created_at__date=created_at_date)

        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = FiveSizePagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = self.queryset

        flight_ids = self.request.query_params.get("flights")

        if self.action != "destroy":
            queryset = Ticket.objects.select_related(
                "order",
                "flight__route__destination__closest_big_city__country",
                "flight__route__source__closest_big_city__country",
                "flight__airplane__airplane_type"
            )

        if flight_ids:
            flight_ids = get_ids(flight_ids)
            queryset = queryset.filter(flight__in=flight_ids)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == "list":
            serializer_class = TicketListSerializer
        elif self.action == "retrieve":
            serializer_class = TicketDetailSerializer

        return serializer_class


class TakenTicketsView(viewsets.ModelViewSet):
    queryset = Ticket.objects.filter(order__isnull=False)
    serializer_class = TakenTicketsSerializer
