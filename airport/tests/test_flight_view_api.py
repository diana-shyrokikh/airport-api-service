from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
)

from airport.serializers import (
    FlightListSerializer,
    FlightDetailSerializer
)

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        request = self.client.get(FLIGHT_URL)

        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@user.com",
            "user123456",
        )

        self.client.force_authenticate(self.user)

        self.countries = [
            Country.objects.create(name=country)
            for country in ("Ukraine", "Italy")
        ]

        self.cities = [
            City.objects.create(
                name="Kyiv",
                country=self.countries[0]
            ),
            City.objects.create(
                name="Rome",
                country=self.countries[1]
            )
        ]

        self.airports = [
            Airport.objects.create(
                name=f"TestAirport{self.cities[i].name}",
                closest_big_city=self.cities[i]
            )
            for i in range(2)
        ]

        self.route = Route.objects.create(
            source=self.airports[0],
            destination=self.airports[1],
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

        self.departure_time_list = [
            datetime(
                2023, 8, 17 + i, 18, 0,
                tzinfo=timezone.utc
            )
            for i in range(2)
        ]
        self.arrival_time_list = [
            datetime(
                2023, 8, 17 + i, 20, 0,
                tzinfo=timezone.utc
            )
            for i in range(2)
        ]

        flights = [
            Flight.objects.create(
                route=self.route,
                airplane=self.airplane,
                departure_time=self.departure_time_list[i],
                arrival_time=self.arrival_time_list[i],
            )
            for i in range(2)
        ]

        for member in self.crew:
            flights[0].crew.add(member)
            flights[1].crew.add(member)

        for flight in flights:
            flight.save()

    def test_flight_list(self):
        request = self.client.get(FLIGHT_URL)

        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        for i in range(2):
            self.assertEqual(
                serializer.data[i]["route"],
                request.data["results"][i]["route"]
            ),
            self.assertEqual(
                serializer.data[i]["airplane"],
                request.data["results"][i]["airplane"]
            ),
            self.assertEqual(
                serializer.data[i]["departure_time"],
                request.data["results"][i]["departure_time"]
            ),
            self.assertEqual(
                serializer.data[i]["arrival_time"],
                request.data["results"][i]["arrival_time"]
            ),

    def test_filter_flights_by_departure_date(self):
        request = self.client.get(
            FLIGHT_URL,
            {"departure_date": f"{self.departure_time_list[0].date()}"}
        )

        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(
            serializer.data[0]["departure_time"],
            request.data["results"][0]["departure_time"]
        ),

        self.assertNotEqual(
            serializer.data[1]["departure_time"],
            request.data["results"][0]["departure_time"]
        ),

    def test_filter_flights_by_arrival_date(self):
        request = self.client.get(
            FLIGHT_URL,
            {"arrival_date": f"{self.arrival_time_list[0].date()}"}
        )

        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(
            serializer.data[0]["arrival_time"],
            request.data["results"][0]["arrival_time"]
        ),

        self.assertNotEqual(
            serializer.data[1]["arrival_time"],
            request.data["results"][0]["arrival_time"]
        ),

    def test_filter_flights_by_destination(self):
        request = self.client.get(
            FLIGHT_URL,
            {"to": f"{self.cities[1].id}"}
        )

        self.countries = self.countries[::-1]
        self.cities = self.cities[::-1]
        self.airports = self.airports[::-1]
        self.route = Route.objects.create(
            source=self.airports[0],
            destination=self.airports[1],
            distance=5000
        )

        Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=self.departure_time_list[0],
            arrival_time=self.arrival_time_list[0],
        )

        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        serializer_destinations = [
            serializer.data[i]["route"].split(" - ")[-1]
            for i in range(3)
        ]

        request_destinations = [
            request.data["results"][i]["route"].split(" - ")[-1]
            for i in range(2)
        ]

        for i in range(2):
            self.assertEqual(
                serializer_destinations[i], request_destinations[i]
            )

            self.assertNotEqual(
                serializer_destinations[2], request_destinations[i]
            )

    def test_filter_flights_by_source(self):
        request = self.client.get(
            FLIGHT_URL,
            {"from": f"{self.cities[0].id}"}
        )

        self.countries = self.countries[::-1]
        self.cities = self.cities[::-1]
        self.airports = self.airports[::-1]
        self.route = Route.objects.create(
            source=self.airports[0],
            destination=self.airports[1],
            distance=5000
        )

        Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=self.departure_time_list[0],
            arrival_time=self.arrival_time_list[0],
        )

        flights = Flight.objects.all()
        serializer = FlightListSerializer(flights, many=True)

        serializer_source1 = serializer.data[0]["route"].split(" - ")[0]
        serializer_source2 = serializer.data[1]["route"].split(" - ")[0]
        serializer_source3 = serializer.data[-1]["route"].split(" - ")[0]
        request_source1 = request.data["results"][0]["route"].split(" - ")[0]
        request_source2 = request.data["results"][1]["route"].split(" - ")[0]

        self.assertEqual(serializer_source1, request_source1)
        self.assertEqual(serializer_source2, request_source2)
        self.assertNotEqual(serializer_source3, request_source1)
        self.assertNotEqual(serializer_source3, request_source2)

    def test_retrieve_flight_detail(self):
        flights = Flight.objects.all()

        url = detail_url(flights[0].id)

        request = self.client.get(url)

        serializer = FlightDetailSerializer(flights[0])

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            serializer.data["route"],
            request.data["route"]
        ),
        self.assertEqual(
            serializer.data["airplane"],
            request.data["airplane"]
        ),
        self.assertEqual(
            serializer.data["departure_time"],
            request.data["departure_time"]
        ),
        self.assertEqual(
            serializer.data["arrival_time"],
            request.data["arrival_time"]
        ),

        for i in range(len(self.crew)):
            self.assertEqual(
                serializer.data["crew"][i],
                request.data["crew"][i]
            ),

    def test_create_flight_forbidden(self):
        payload = {
            "route": self.route,
            "airplane": self.airplane,
            "departure_time": self.departure_time_list[0],
            "arrival_time": self.arrival_time_list[0],
        }

        request = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="admin123456",
            is_staff=True,
        )

        self.client.force_authenticate(self.admin)

        self.countries = [
            Country.objects.create(name=country)
            for country in ("Ukraine", "Italy")
        ]

        self.cities = [
            City.objects.create(
                name="Kyiv",
                country=self.countries[0]
            ),
            City.objects.create(
                name="Rome",
                country=self.countries[1]
            )
        ]

        self.airports = [
            Airport.objects.create(
                name=f"TestAirport{self.cities[i].name}",
                closest_big_city=self.cities[i]
            )
            for i in range(2)
        ]

        self.route = Route.objects.create(
            source=self.airports[0],
            destination=self.airports[1],
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

        self.departure_time = "2023-08-17 18:00"
        self.arrival_time = "2023-08-17 20:00"

    def test_create_flight(self):
        payload = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
        }

        request = self.client.post(FLIGHT_URL, payload)
        flight = Flight.objects.get(id=request.data["id"])

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            flight.route.id,
            request.data["route"]
        ),
        self.assertEqual(
            flight.airplane.id,
            request.data["airplane"]
        ),

        request_departure_time = datetime.strptime(
            request.data["departure_time"],
            "%Y-%m-%dT%H:%M:%SZ"
        )
        request_departure_time_naive = request_departure_time.replace(
            tzinfo=None
        )

        self.assertEqual(
            flight.departure_time.replace(tzinfo=None),
            request_departure_time_naive
        ),

        request_arrival_time = datetime.strptime(
            request.data["arrival_time"],
            '%Y-%m-%dT%H:%M:%SZ'
        )
        request_arrival_time_naive = request_arrival_time.replace(
            tzinfo=None
        )

        self.assertEqual(
            flight.arrival_time.replace(tzinfo=None),
            request_arrival_time_naive
        ),

    def test_create_flight_with_crew(self):

        payload = {
            "route": self.route.id,
            "airplane": self.airplane.id,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "crew": [
                crew.id
                for crew in self.crew
            ]
        }

        request = self.client.post(FLIGHT_URL, payload)
        flight = Flight.objects.get(id=request.data["id"])

        crew = flight.crew.all()

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        self.assertEqual(crew.count(), 5)
        for crew_member in self.crew:
            self.assertIn(crew_member, crew)

    def test_delete_flight_not_allowed(self):
        flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=datetime(
                2023, 8, 17, 18, 0,
                tzinfo=timezone.utc
            ),
            arrival_time=datetime(
                2023, 8, 17, 20, 0,
                tzinfo=timezone.utc
            )
        )

        url = detail_url(flight.id)

        request = self.client.delete(url)

        self.assertEqual(
            request.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
