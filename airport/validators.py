import re
from datetime import datetime

from django.utils import timezone

from airport.helper import WeatherAPI

NAME_PATTERN = r"^(?=.*[a-zA-Z])[a-zA-Z\s]+$"
AIRPORT_NAME_PATTERN = r"^(?=.*[a-zA-Z])[a-zA-Z\s.()-/]+$"
AIRPLANE_NAME_PATTERN = r"^(?!^[0-9])^(?=.*[a-zA-Z])[a-zA-Z0-9\s]+$"


def validate_city_country(
        city: str,
        country: str,
        error_to_raise
):
    weather_api = WeatherAPI()
    country_name = weather_api.get_country(city)

    if country_name == "error":
        raise error_to_raise({
            "name": "The city doesn't exist"
        })

    if country.lower() != country_name.lower():
        raise error_to_raise({
            "country": "The city is not on the territory "
                       "of the country"
        })


def validate_name(
        name: str,
        error_to_raise,
        field_name: str = "name"
):

    if re.search(NAME_PATTERN, name) is None:
        raise error_to_raise({
            f"{field_name}": f"{name} should contain only "
                             f"english letters also spaces are allowed"
        })


def validate_airport_name(
        name: str,
        error_to_raise,
        field_name: str = "name"
):

    if re.search(AIRPORT_NAME_PATTERN, name) is None:
        raise error_to_raise({
            f"{field_name}": f"{name} should contain english letters "
                             f"also spaces, parentheses and "
                             f"symbols: - . /  are allowed"
        })


def validate_airplane(name: str, error_to_raise):
    if re.search(AIRPLANE_NAME_PATTERN, name) is None:
        raise error_to_raise({
            "name": f"{name} should contain english letters "
                    f"with or without space and digits"
        })


def validate_source_and_destination_is_not_equal(
    source_id: int,
    destination_id: int,
    error_to_raise
):
    if source_id == destination_id:
        raise error_to_raise({
            "source": "Source and destination should not be the same",
            "destination": "Destination and source should not be the same"
        })


def validate_date(
        field_name: str,
        date: datetime,
        error_to_raise
):
    if timezone.now() > date:
        raise error_to_raise({
            f"{field_name}": f"{date} shouldn't be in the past"
        })


def validate_date_is_not_equal(
        first_date_field_name: str,
        second_date_field_name: str,
        first_date: datetime,
        second_date: datetime,
        error_to_raise
):
    if first_date == second_date:
        raise error_to_raise({
            f"{first_date_field_name}":
                f"{first_date_field_name} & {second_date_field_name} "
                f"shouldn't be the same",
            f"{second_date_field_name}":
                f"{first_date_field_name} & {second_date_field_name} "
                f"shouldn't be the same",
        })


def validate_departure_arrival_date(
        departure_time: datetime,
        arrival_time: datetime,
        error_to_raise
):
    if departure_time > arrival_time:
        raise error_to_raise({
            "departure_time":
                "departure time should not be later than arrival time",
        })


def validate_seat_or_row(
        field_name: str,
        seat_or_row: int,
        seats_or_rows: int,
        error_to_raise
):
    if seat_or_row > seats_or_rows:
        raise error_to_raise({
            f"{field_name}":
                f"{seat_or_row} must be "
                f"in range (1, {seats_or_rows})"
        })
