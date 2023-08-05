from django.core.exceptions import ValidationError
from django.db import models

from pycountry import countries

from airport.validators import (
    validate_name,
    validate_airplane_name,
    validate_date,
    validate_date_is_not_equal, validate_source_and_destination_is_not_equal
)
from user.models import User


# from order_tickets.models import Ticket


class Country(models.Model):
    COUNTRY_CHOICES = [
        (country.name, country.name)
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

        self.name = self.name.capitalize()

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

    def __str__(self):
        return self.name

    def clean(self):
        validate_name(name=self.name, error_to_raise=ValidationError)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.capitalize()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Airport(models.Model):
    name = models.CharField(unique=True, max_length=63)
    city = models.ForeignKey(
        City,
        related_name="airports",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.city} ({self.name})"

    class Meta:
        unique_together = ("name", "city")

    def clean(self):
        validate_name(name=self.name, error_to_raise=ValidationError)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.capitalize()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Route(models.Model):
    source = models.ForeignKey(
        City,
        related_name="routs_source",
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        City,
        related_name="routs_destination",
        on_delete=models.CASCADE
    )
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = ("source", "destination")

    def __str__(self):
        return f"{self.source} - {self.destination}"

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
        validate_name(name=self.name, error_to_raise=ValidationError)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()

        self.name = self.name.capitalize()

        return super().save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )


class Airplane(models.Model):
    name = models.CharField(unique=True, max_length=63)
    rows = models.PositiveIntegerField()
    seats_in_rows = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        related_name="airplanes",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [
            ("rows", "seats_in_rows"),
            ("name", "airplane_type")
        ]
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.airplane_type})"

    def clean(self):
        validate_airplane_name(
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

        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

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
    ticket = models.ForeignKey(
        to="Ticket",
        related_name="flights",
        on_delete=models.CASCADE
    )
    crew = models.ManyToManyField(Crew, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        unique_together = ("route", "airplane", "departure_time")

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

    def __str__(self):
        return f"Ticket: row {self.row}, seat{self.seat}"

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
                    f"in range (1, {seats_or_rows}"
            })

    def clean(self):
        Ticket.validate_seat_or_row(
            field_name="row",
            seat_or_row=self.row,
            seats_or_rows=Flight.airplane.rows,
            error_to_raise=ValidationError
        )
        Ticket.validate_seat_or_row(
            field_name="seat",
            seat_or_row=self.seat,
            seats_or_rows=Flight.airplane.seats_in_rows,
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
