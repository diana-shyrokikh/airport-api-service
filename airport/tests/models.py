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

