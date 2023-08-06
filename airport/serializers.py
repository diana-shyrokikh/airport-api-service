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


class TicketSerializer(serializers.ModelSerializer):
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

# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ("id", "row", "seat", "flight")
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     tickets = TicketSerializer(
#         read_only=False,
#         many=False,
#         # allow_empty=False
#     )
#
#     class Meta:
#         model = Order
#         fields = (
#             "id",
#             "tickets",
#             "created_at",
#             "user"
#         )
#
#     def create(self, validated_data):
#         with transaction.atomic():
#             tickets_data = validated_data.pop("tickets")
#             print(tickets_data)
#             tickets_data["flight"] = tickets_data["flight"].id
#             order = Order.objects.create(**validated_data)
#             # ticket_data = tickets_data  # Remove this line since tickets_data is not a dictionary anymore
#             # Ticket.objects.create(
#             #     order=order,
#             #     row=ticket_data["row"],  # Access the fields through the nested serializer
#             #     seat=ticket_data["seat"],  # Access the fields through the nested serializer
#             #     flight=ticket_data["flight"],  # Access the fields through the nested serializer
#             # )
#             ticket_serializer = TicketSerializer(data=tickets_data)
#             ticket_serializer.is_valid(raise_exception=True)
#             ticket_serializer.save(order=order)
#             return order
