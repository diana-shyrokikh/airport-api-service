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
from airport.validators import (
    validate_name,
    validate_airplane,
    validate_date,
    validate_date_is_not_equal,
    validate_source_and_destination_is_not_equal,
    validate_airport_name,
    validate_departure_arrival_date
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CountryListSerializer(CountrySerializer):
    cities = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Country
        fields = ("id", "name", "cities")


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"

    def validate(self, attrs):
        data = super(CitySerializer, self).validate(attrs)

        validate_name(
            name=attrs["name"],
            error_to_raise=serializers.ValidationError
        )

        return data


class CityListSerializer(CitySerializer):
    country = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityDetailSerializer(CitySerializer):
    country = CountrySerializer(many=False, read_only=True)
    airports = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = City
        fields = ("id", "name", "country", "airports")


class AirportCityDetailSerializer(CitySerializer):
    country = CountrySerializer(many=False, read_only=True)

    class Meta:
        model = City
        fields = ("name", "country")


class CountryCityDetailSerializer(CitySerializer):
    airports = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = City
        fields = ("name", "airports")


class CountryDetailSerializer(CountrySerializer):
    cities = CountryCityDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ("id", "name", "cities")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"

    def validate(self, attrs):
        data = super(AirportSerializer, self).validate(attrs)

        validate_airport_name(
            name=attrs["name"],
            error_to_raise=serializers.ValidationError
        )

        return data


class AirportListSerializer(AirportSerializer):
    closest_big_city = serializers.CharField(source="closest_big_city.name", read_only=True)
    country = serializers.CharField(source="closest_big_city.country.name", read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "country")


class AirportDetailSerializer(AirportSerializer):
    closest_big_city = AirportCityDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

    def validate(self, attrs):
        data = super(RouteSerializer, self).validate(attrs)

        validate_source_and_destination_is_not_equal(
            source_id=attrs["source"].id,
            destination_id=attrs["destination"].id,
            error_to_raise=serializers.ValidationError
        )

        return data


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    destination = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "name", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = AirportDetailSerializer(many=False, read_only=True)
    destination = AirportDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = ("id", "name", "source", "destination", "distance")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"

    def validate(self, attrs):
        data = super(AirplaneTypeSerializer, self).validate(attrs)

        validate_airplane(
            name=attrs["name"],
            error_to_raise=serializers.ValidationError
        )

        return data


class AirplaneTypeListSerializer(AirplaneTypeSerializer):
    airplanes = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )

    class Meta:
        model = AirplaneType
        fields = ("id", "name", "airplanes")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"

    def validate(self, attrs):
        data = super(AirplaneSerializer, self).validate(attrs)

        validate_airplane(
            name=attrs["name"],
            error_to_raise=serializers.ValidationError
        )

        return data


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name", read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane_type",
            "airplane_capacity",
            "rows",
            "seats_in_rows",
        )


class AirplaneTypeAirplaneListSerializer(AirplaneSerializer):
    class Meta:
        model = Airplane
        fields = ("name", "rows", "seats_in_rows", "airplane_capacity")


class AirplaneTypeDetailSerializer(AirplaneTypeSerializer):
    airplanes = AirplaneTypeAirplaneListSerializer(many=True, read_only=True)

    class Meta:
        model = AirplaneType
        fields = ("id", "name", "airplanes")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"

    def validate(self, attrs):
        data = super(CrewSerializer, self).validate(attrs)

        validate_name(
            field_name="first_name",
            name=attrs["first_name"],
            error_to_raise=serializers.ValidationError
        )
        validate_name(
            field_name="last_name",
            name=attrs["last_name"],
            error_to_raise=serializers.ValidationError
        )

        return data


class CrewListSerializer(CrewSerializer):
    class Meta:
        model = Crew
        fields = ("id", "full_name")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"

    def validate(self, attrs):
        data = super(FlightSerializer, self).validate(attrs)

        validate_date(
            field_name="departure_time",
            date=attrs["departure_time"],
            error_to_raise=serializers.ValidationError
        )
        validate_date(
            field_name="arrival_time",
            date=attrs["arrival_time"],
            error_to_raise=serializers.ValidationError
        )
        validate_date_is_not_equal(
            first_date_field_name="departure_time",
            second_date_field_name="arrival_time",
            first_date=attrs["departure_time"],
            second_date=attrs["arrival_time"],
            error_to_raise=serializers.ValidationError
        )
        validate_departure_arrival_date(
            departure_time=attrs["departure_time"],
            arrival_time=attrs["arrival_time"],
            error_to_raise=serializers.ValidationError
        )

        return data


class TakenTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightListSerializer(FlightSerializer):
    route = serializers.CharField(source="route.name", read_only=True,)
    airplane = serializers.CharField(source="airplane.name", read_only=True,)
    airplane_capacity = serializers.IntegerField(
        source="airplane.airplane_capacity",
        read_only=True,
    )
    tickets_available = serializers.IntegerField(read_only=True)
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
            "tickets_available",
            "crew",
        )


class FlightDetailSerializer(FlightListSerializer):
    route = RouteListSerializer(many=False, read_only=True,)
    airplane = AirplaneListSerializer(many=False, read_only=True,)
    crew = CrewListSerializer(many=True, read_only=True,)
    taken_places = TakenTicketsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "flight_duration",
            "departure_time",
            "arrival_time",
            "tickets_available",
            "crew",
            "taken_places",
        )


class MiniFlightDetailSerializer(FlightListSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "flight_duration",
            "departure_time",
            "arrival_time",
        )


class AirplaneDetailSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)
    flights = MiniFlightDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane_type",
            "rows",
            "seats_in_rows",
            "airplane_capacity",
            "flights"
        )


class CrewDetailSerializer(CrewSerializer):
    flights = MiniFlightDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "flights")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)

        Ticket.validate_seat_or_row(
            field_name="row",
            seat_or_row=attrs["row"],
            seats_or_rows=attrs["flight"].airplane.rows,
            error_to_raise=serializers.ValidationError
        )
        Ticket.validate_seat_or_row(
            field_name="seat",
            seat_or_row=attrs["seat"],
            seats_or_rows=attrs["flight"].airplane.seats_in_rows,
            error_to_raise=serializers.ValidationError
        )

        return data


class TicketListSerializer(TicketSerializer):
    flight = serializers.CharField(source="flight.route.name", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketDetailSerializer(TicketSerializer):
    flight = MiniFlightDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at",)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")

            order = Order.objects.create(**validated_data)

            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at",)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at",)
