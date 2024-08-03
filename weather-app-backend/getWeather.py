import openmeteo_requests
from openmeteo_sdk.Variable import Variable

import requests_cache
import pandas as pd
from retry_requests import retry

def cache_weather():
    # Setting up the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    return retry_session

def get_current_weather(latitude = 52.54, longitude = 13.41):
    session = cache_weather()
    openmeteo = openmeteo_requests.Client(session = session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "apparent_temperature", "is_day", "precipitation", "weather_code"],
        "hourly": "temperature_2m",
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "precipitation_sum"],
        "temperature_unit": "fahrenheit"
    }
    responses = openmeteo.weather_api(url, params = params)

    # just processing the first location as response might give multiple locations
    response = responses[0]
    current = response.Current()
    return current

if __name__ == '__main__':
    get_current_weather()