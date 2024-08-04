import openmeteo_requests
from openmeteo_sdk.Variable import Variable

import requests_cache
import pandas as pd
import numpy as np

from retry_requests import retry

def cache_weather():
    # Setting up the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    return retry_session

def get_weather_response(latitude = 52.54, longitude = 13.41):
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
    return response

def hourly_forecast_df(response):
    hourly = response.Hourly()
    hourly_time = range(hourly.Time(), hourly.TimeEnd(), hourly.Interval())
    hourly_variables = list(map(lambda i: hourly.Variables(i), range(0, hourly.VariablesLength())))

    hourly_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, hourly_variables)).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s"),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe_pd = pd.DataFrame(data = hourly_data)
    for i in range(1, 5):
        print(f"{hourly_dataframe_pd['date'][i]} -> {hourly_dataframe_pd['temperature_2m'][i]}")
        print()

    return hourly_dataframe_pd

if __name__ == '__main__':
    response = get_weather_response(42.4,-71.05)
    hourly_forecast_df(response)