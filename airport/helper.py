import json
import os

import requests
from dotenv import load_dotenv

from rest_framework import status


load_dotenv()


class WeatherAPI:
    BASE_URL = "http://api.weatherapi.com/v1/current.json"

    def __init__(self):
        self.api_key = os.environ["API_KEY"]

    def get_country(self, city: str):

        # Unfortunately, api does not know
        # the correct name of the capital of Ukraine
        if city.capitalize() == "Kyiv":
            city = "Kiev"

        params = {
            "q": city,
            "key": self.api_key,
        }

        request_ = requests.get(self.BASE_URL, params=params)

        json_result = json.loads(request_.content)
        if request_.status_code == status.HTTP_200_OK:
            return json_result["location"]["country"]

        if request_.status_code == status.HTTP_400_BAD_REQUEST:
            return "error"


def get_ids(queryset):
    return [
        object_id
        for object_id in queryset.split(",")
    ]
