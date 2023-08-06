from django.db import transaction
from rest_framework import serializers

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


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class CityListSerializer(CitySerializer):
    country = serializers.CharField(source="country.name")

    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityDetailSerializer(CitySerializer):
    country = CountrySerializer(many=False)

    class Meta:
        model = City
        fields = ("id", "name", "country")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirportListSerializer(AirportSerializer):
    closest_big_city = serializers.CharField(source="closest_big_city.name")
    country = serializers.CharField(source="closest_big_city.country.name")

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "country")


class AirportDetailSerializer(AirportSerializer):
    closest_big_city = CityDetailSerializer(many=False)

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name")
    destination = serializers.CharField(source="destination.name")

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "name", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = AirportDetailSerializer(many=False)
    destination = AirportDetailSerializer(many=False)

    class Meta:
        model = Route
        fields = ("id", "name", "source", "destination", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name")

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_capacity", "airplane_type")


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False)

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_capacity", "airplane_type")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class CrewListSerializer(CrewSerializer):
    class Meta:
        model = Crew
        fields = ("id", "full_name")


class CrewDetailSerializer(CrewSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class FlightListSerializer(FlightSerializer):
    route = serializers.CharField(source="route.name")
    airplane = serializers.CharField(source="airplane.name")
    airplane_capacity = serializers.IntegerField(source="airplane.airplane_capacity")
    crew = serializers.SlugRelatedField(
        slug_field="full_name",
        many=True,
        read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "airplane_capacity",
            "flight_duration",
            "departure_time",
            "arrival_time",
            "crew"
        )


class FlightDetailSerializer(FlightListSerializer):
    route = RouteListSerializer(many=False)
    airplane = AirplaneListSerializer(many=False)
    crew = CrewListSerializer(many=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "flight_duration",
            "departure_time",
            "arrival_time",
            "crew"
        )


class TicketFlightListSerializer(FlightSerializer):
    route = serializers.CharField(source="route.name")
    airplane_capacity = serializers.IntegerField(source="airplane.airplane_capacity")

    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane_capacity",
            "flight_duration",
            "departure_time",
            "arrival_time",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    flight = serializers.CharField(source="flight.route.name")

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketDetailSerializer(TicketSerializer):
    flight = TicketFlightListSerializer(many=False)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at",)

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")

        order = Order.objects.create(**validated_data)

        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)

        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at",)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at",)
