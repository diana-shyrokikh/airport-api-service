import json

import requests

from rest_framework import status

URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = "38c3ebe8bd6447ad811133507230208"


def get_country(city: str):

    # Unfortunately, api does not know
    # the correct name of the capital of Ukraine
    if city.capitalize() == "Kyiv":
        city = "Kiev"

    params = {
        "q": city,
        "key": API_KEY,
    }

    request_ = requests.get(URL, params=params)

    json_result = json.loads(request_.content)
    if request_.status_code == status.HTTP_200_OK:
        return json_result["location"]["country"]

    if request_.status_code == status.HTTP_400_BAD_REQUEST:
        return "error"
