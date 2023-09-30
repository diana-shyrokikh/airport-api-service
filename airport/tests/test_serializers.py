from django.test import TestCase

from airport.models import (
    Country,
    City,
    Airport,
    AirplaneType,
)
from airport.serializers import (
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer
)


class CitySerializerTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine")
        self.city_data = {
            "name": "Lviv",
            "country": self.country.id
        }

    def test_valid_city_data(self):
        serializer = CitySerializer(data=self.city_data)

        self.assertTrue(serializer.is_valid())

    def test_invalid_name_city(self):

        invalid_names = ["   ", "123Kyiv", ".,", "Kyiv_"]

        for name in invalid_names:
            self.city_data["name"] = name
            serializer = CitySerializer(data=self.city_data)
            self.assertFalse(serializer.is_valid())

    def test_invalid_city_country(self):
        self.city_data["name"] = "Rome"
        serializer = CitySerializer(data=self.city_data)
        self.assertFalse(serializer.is_valid())


class AirportSerializerTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine")
        self.city = City.objects.create(name="Kyiv", country=self.country)
        self.airport_data = {
            "name": "Test-Airport/International(TestTest)",
            "closest_big_city": self.city.id
        }

    def test_valid_name_airport(self):
        serializer = AirportSerializer(data=self.airport_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_name_airport(self):
        invalid_names = ["   ", "123Test", ".,", "Test_"]

        for name in invalid_names:
            self.airport_data["name"] = name
            serializer = AirportSerializer(data=self.airport_data)
            self.assertFalse(serializer.is_valid())


class RouteSerializerTests(TestCase):
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
        self.route_data = {
            "source": self.airport1.id,
            "destination": self.airport2.id,
            "distance": 5000,
        }

    def test_valid_source_and_destination(self):
        serializer = RouteSerializer(data=self.route_data)

        self.assertTrue(serializer.is_valid())

    def test_validate_source_and_destination_is_not_equal(self):
        self.route_data["destination"] = self.airport1.id
        serializer = RouteSerializer(data=self.route_data)

        self.assertFalse(serializer.is_valid())


class AirplaneTypeSerializerTests(TestCase):
    def setUp(self):
        self.airplane_type_data = {
            "name": "TestAirplaneType AT28",
        }

    def test_valid_airplane_type_name(self):
        serializer = AirplaneTypeSerializer(data=self.airplane_type_data)

        self.assertTrue(serializer.is_valid())

    def test_invalid_airplane_type_name(self):
        invalid_names = ["   ", "123Test", ".,", "Test_"]

        for name in invalid_names:
            self.airplane_type_data["name"] = name
            serializer = AirplaneTypeSerializer(data=self.airplane_type_data)

            self.assertFalse(serializer.is_valid())


class AirplaneSerializerTests(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(
            name="TestAirplaneType AT28",
        )
        self.airplane_data = {
            "name": "Test Airplane 28",
            "airplane_type": self.airplane_type.id,
            "rows": 10,
            "seats_in_row": 5,
        }

    def test_valid_airplane_name(self):
        serializer = AirplaneSerializer(data=self.airplane_data)

        self.assertTrue(serializer.is_valid())

    def test_invalid_airplane_name(self):
        invalid_names = ["   ", "123Test", ".,", "Test_"]

        for name in invalid_names:
            self.airplane_data["name"] = name
            serializer = AirplaneSerializer(data=self.airplane_data)

            self.assertFalse(serializer.is_valid())


class CrewSerializerTests(TestCase):
    def setUp(self):
        self.crew_data = {
            "first_name": "Test First Name",
            "last_name": "Test Last Name",
        }

    def test_valid_names(self):
        serializer = CrewSerializer(data=self.crew_data)

        self.assertTrue(serializer.is_valid())

    def test_invalid_names(self):
        invalid_names = ["   ", "123Test", ".,", "Test_"]

        for name in invalid_names:
            crew_data = {
                "first_name": "Test First Name",
                "last_name": name,
            }

            serializer = CrewSerializer(data=crew_data)

            self.assertFalse(serializer.is_valid())

        for name in invalid_names:
            crew_data = {
                "last_name": "Test Last Name",
                "first_name": name,
            }

            serializer = CrewSerializer(data=crew_data)

            self.assertFalse(serializer.is_valid())
