import re
from datetime import datetime

from django.utils import timezone


NAME_PATTERN = r"^(?=.*[a-zA-Z])[a-zA-Z\s]+$"
AIRPORT_NAME_PATTERN = r"^(?=.*[a-zA-Z])[a-zA-Z\s.()-/]+$"
AIRPLANE_NAME_PATTERN = r"^(?=.*[a-zA-Z])[a-zA-Z0-9\s]+$"


def validate_name(
        name: str,
        error_to_raise,
        field_name: str = "name"
):

    if re.search(NAME_PATTERN, name) is None:
        raise error_to_raise({
            f"{field_name}": f"{name} should contain only english letters also spaces are allowed"
        })


def validate_airport_name(
        name: str,
        error_to_raise,
        field_name: str = "name"
):

    if re.search(AIRPORT_NAME_PATTERN, name) is None:
        raise error_to_raise({
            f"{field_name}": f"{name} should contain english letters "
                             f"also spaces, parentheses and symbols: - . /  are allowed"
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
