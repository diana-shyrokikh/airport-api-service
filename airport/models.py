from django.core.exceptions import ValidationError
from django.db import models

from pycountry import countries

from airport.validators import (
    validate_name,
    validate_airplane,
    validate_date,
    validate_date_is_not_equal,
    validate_source_and_destination_is_not_equal,
    validate_airport_name,
    validate_departure_arrival_date, validate_city_country
)
from user.models import User


class Country(models.Model):
    COUNTRY_CHOICES = [
        (
            country.name.title().split(",")[0],
            country.name.title().split(",")[0]
        )
        for country in list(countries)
    ]

    name = models.CharField(
        max_length=63,
        unique=True,
        choices=COUNTRY_CHOICES,
    )

    class Meta:
        verbose_name_plural = "countries"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.title().strip()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class City(models.Model):
    name = models.CharField(max_length=63)
    country = models.ForeignKey(
        Country,
        related_name="cities",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("name", "country")
        ordering = ["name"]
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name

    def clean(self):
        validate_name(name=self.name, error_to_raise=ValidationError)
        validate_city_country(
            city=self.name,
            country=self.country.name,
            error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.strip()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Airport(models.Model):
    name = models.CharField(unique=True, max_length=63)
    closest_big_city = models.ForeignKey(
        City,
        related_name="airports",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "closest_big_city")

    def clean(self):
        validate_airport_name(name=self.name, error_to_raise=ValidationError)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.title().strip()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        related_name="routs_source",
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Airport,
        related_name="routs_destination",
        on_delete=models.CASCADE
    )
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = ("source", "destination")

    @property
    def name(self):
        return (
            f"{self.source.closest_big_city.name} "
            f"- {self.destination.closest_big_city.name}"
        )

    def __str__(self):
        return (
            f"{self.source} - {self.destination}"
        )

    def clean(self):
        validate_source_and_destination_is_not_equal(
            source_id=self.source.id,
            destination_id=self.destination.id,
            error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class AirplaneType(models.Model):
    name = models.CharField(unique=True, max_length=63)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        validate_airplane(name=self.name, error_to_raise=ValidationError)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.strip()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Airplane(models.Model):
    name = models.CharField(unique=True, max_length=63)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        related_name="airplanes",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [
            ("name", "airplane_type")
        ]
        ordering = ["name"]

    @property
    def airplane_capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name

    def clean(self):
        validate_airplane(
            name=self.name, error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.strip()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    class Meta:
        unique_together = ("first_name", "last_name")
        ordering = ["last_name"]

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        validate_name(
            field_name="first_name",
            name=self.first_name,
            error_to_raise=ValidationError
        )
        validate_name(
            field_name="last_name",
            name=self.last_name,
            error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.first_name = self.first_name.title().strip()
        self.last_name = self.last_name.title().strip()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        related_name="flights",
        on_delete=models.CASCADE
    )
    airplane = models.ForeignKey(
        Airplane,
        related_name="flights",
        on_delete=models.CASCADE
    )
    crew = models.ManyToManyField(
        Crew,
        related_name="flights",
        blank=True
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        unique_together = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time"
        )

    @property
    def flight_duration(self):
        seconds_in_hour = 3600
        return (self.arrival_time - self.departure_time).total_seconds() / seconds_in_hour

    def __str__(self) -> str:
        return f"{self.route} ({self.departure_time})"

    def clean(self):
        validate_date(
            field_name="departure_time",
            date=self.departure_time,
            error_to_raise=ValidationError
        )
        validate_date(
            field_name="arrival_time",
            date=self.arrival_time,
            error_to_raise=ValidationError
        )
        validate_date_is_not_equal(
            first_date_field_name="departure_time",
            second_date_field_name="arrival_time",
            first_date=self.departure_time,
            second_date=self.arrival_time,
            error_to_raise=ValidationError
        )
        validate_departure_arrival_date(
            departure_time=self.departure_time,
            arrival_time=self.arrival_time,
            error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Order №{self.id}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight, related_name="tickets", on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order, related_name="tickets", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("row", "seat", "flight"),

    def __str__(self):
        return f"Ticket: row {self.row}, seat {self.seat}"

    @staticmethod
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

    def clean(self):
        Ticket.validate_seat_or_row(
            field_name="row",
            seat_or_row=self.row,
            seats_or_rows=self.flight.airplane.rows,
            error_to_raise=ValidationError
        )
        Ticket.validate_seat_or_row(
            field_name="seat",
            seat_or_row=self.seat,
            seats_or_rows=self.flight.airplane.seats_in_row,
            error_to_raise=ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )
