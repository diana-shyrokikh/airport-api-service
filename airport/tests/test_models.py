from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

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
)


class CountryModelTests(TestCase):

    def test_country_str(self):
        country = Country.objects.create(name="Ukraine")

        self.assertEqual(country.name, str(country))


class CityModelTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine")

    def test_city_str(self):
        city = City.objects.create(name="Kyiv", country=self.country)

        self.assertEqual(city.name, str(city))


class AirportModelTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine")
        self.city = City.objects.create(name="Kyiv", country=self.country)

    def test_airport_str(self):
        airport = Airport.objects.create(
            name="Test-Airport/International(TestTest)",
            closest_big_city=self.city,
        )

        self.assertEqual(airport.name, str(airport))


class RouteModelTests(TestCase):
    def setUp(self):
        self.country1 = Country.objects.create(name="Ukraine")
        self.country2 = Country.objects.create(name="Italy")

        self.city1 = City.objects.create(name="Kyiv", country=self.country1)
        self.city2 = City.objects.create(name="Rome", country=self.country2)

        self.airport1 = Airport.objects.create(
            name="FirstTestAirport", closest_big_city=self.city1
        )
        self.airport2 = Airport.objects.create(
            name="SecondTestAirport", closest_big_city=self.city2
        )

    def test_route_str(self):
        route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=5000,
        )

        string = f"{route.source} - {route.destination}"

        self.assertEqual(string, str(route))


class AirplaneTypeModelTests(TestCase):
    def test_airplane_type_str(self):
        airplane_type = AirplaneType.objects.create(
            name="TestAirplaneType AT28",
        )

        self.assertEqual(airplane_type.name, str(airplane_type))


class AirplaneModelTests(TestCase):
    def setUp(self):
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

        self.assertEqual(airplane.name, str(airplane))


class CrewModelTests(TestCase):

    def test_crew_str(self):
        crew = Crew.objects.create(
            first_name="Test First Name",
            last_name="Test Last Name",

        )

        self.assertEqual(
            f"{crew.first_name} {crew.last_name}",
            str(crew)
        )


class FlightTicketOrderModelTests(TestCase):
    def setUp(self):
        self.country1 = Country.objects.create(name="Ukraine")
        self.country2 = Country.objects.create(name="Italy")

        self.city1 = City.objects.create(name="Kyiv", country=self.country1)
        self.city2 = City.objects.create(name="Rome", country=self.country2)

        self.airport1 = Airport.objects.create(
            name="FirstTestAirport", closest_big_city=self.city1
        )
        self.airport2 = Airport.objects.create(
            name="SecondTestAirport", closest_big_city=self.city2
        )

        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=5000
        )

        self.airplane_type = AirplaneType.objects.create(
            name="TestAirplaneType AT28",
        )
        self.airplane = Airplane.objects.create(
            name="TestAirplane",
            rows=50,
            seats_in_row=11,
            airplane_type=self.airplane_type
        )
        self.crew = [
            Crew.objects.create(
                first_name=f"Test {letter}",
                last_name="TestLast"
            )
            for letter in "abcde"
        ]

        self.departure_time = datetime(
            2023, 8, 17, 18, 0,
            tzinfo=timezone.utc
        )
        self.arrival_time = datetime(
            2023, 8, 17, 20, 0,
            tzinfo=timezone.utc
        )

        self.user = get_user_model().objects.create_user(
            email="test@post.com",
            password="user123456"
        )

        self.order = Order.objects.create(user=self.user)

    def test_flight_str(self):
        flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=self.departure_time,
            arrival_time=self.arrival_time
        )

        for member in self.crew:
            flight.crew.add(member)

        flight.save()

        self.assertEqual(
            f"{flight.route} ({flight.departure_time})",
            str(flight)
        )
