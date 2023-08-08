from django.core.exceptions import ValidationError
from django.test import TestCase

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


class CountryModelTests(TestCase):

    def test_country_str(self):
        country = Country.objects.create(name="Ukraine")

        self.assertEqual(country.name, str(country))


class CityModelTests(TestCase):
    def setUp(self) -> None:
        self.country = Country.objects.create(name="Ukraine")

    def test_city_str(self):
        city = City.objects.create(name="Kyiv", country=self.country)

        self.assertEqual(city.name, str(city))

    def test_validate_name_city(self):
        invalid_names = ["   ", "123Kyiv", ".,", "Kyiv_"]

        for name in invalid_names:
            with self.assertRaises(ValidationError):
                City.objects.create(name=name, country=self.country)


class AirportModelTests(TestCase):
    def setUp(self) -> None:
        self.country = Country.objects.create(name="Ukraine")
        self.city = City.objects.create(name="Kyiv", country=self.country)

    def test_airport_str(self):
        airport = Airport.objects.create(
            name="Test-Airport/International(TestTest)",
            closest_big_city=self.city,
        )

        self.assertEqual(
            f"{airport.name} ({airport.closest_big_city.name})",
            str(airport)
        )

    def test_validate_airport_name(self):
        invalid_names = ["   ", "123Test", ".,", "Test_"]

        for name in invalid_names:
            with self.assertRaises(ValidationError):
                Airport.objects.create(name=name, closest_big_city=self.city)


class RouteModelTests(TestCase):
    def setUp(self) -> None:
        self.country1 = Country.objects.create(name="Ukraine")
        self.country2 = Country.objects.create(name="Italy")

        self.city1 = City.objects.create(name="Kyiv", country=self.country1)
        self.city2 = City.objects.create(name="Rome", country=self.country2)

        self.airport1 = Airport.objects.create(name="FirstTestAirport", closest_big_city=self.city1)
        self.airport2 = Airport.objects.create(name="SecondTestAirport", closest_big_city=self.city2)

    def test_route_str(self):
        route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=5000,
        )

        string = (
            f"{route.source.closest_big_city.name} "
            f"- {route.destination.closest_big_city.name}"
        )
        self.assertEqual(string, str(route))

    def test_validate_source_and_destination_is_not_equal(self):
        with self.assertRaises(ValidationError):
            Route.objects.create(
                source=self.airport1,
                destination=self.airport1,
                distance=1000
            )


class AirplaneTypeModelTests(TestCase):
    def test_airplane_type_str(self):
        airplane_type = AirplaneType.objects.create(
            name="TestAirplaneType AT28",
        )

        self.assertEqual(airplane_type.name, str(airplane_type))

    def test_validate_airplane(self):
        invalid_names = ["   ", "123Test", ".,", "Test_"]

        for name in invalid_names:
            with self.assertRaises(ValidationError):
                AirplaneType.objects.create(name=name)


class AirplaneModelTests(TestCase):
    def setUp(self) -> None:
        self.airplane_type = AirplaneType.objects.create(
            name="TestAirplaneType AT28",
        )

    def test_airplane_str(self):
        airplane = Airplane.objects.create(
            name="Test Airplane 28",
            airplane_type=self.airplane_type,
            rows=10,
            seats_in_row=5,
        )

        self.assertEqual(
            f"{airplane.name} ({airplane.airplane_type})",
            str(airplane)
        )

    def test_validate_airplane(self):
        invalid_names = ["   ", "123Test", ".,", "Test_"]

        for name in invalid_names:
            with self.assertRaises(ValidationError):
                Airplane.objects.create(
                    name=name,
                    airplane_type=self.airplane_type,
                    rows=10,
                    seats_in_row=5,
                )
