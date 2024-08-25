import openmeteo_requests
from openmeteo_sdk.Variable import Variable

import requests_cache
import pandas as pd
import numpy as np

from retry_requests import retry

import datetime

from collections import OrderedDict

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
        "current": ["temperature_2m", "apparent_temperature", "is_day", "precipitation", "weather_code", "rain"],
        "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "weather_code"],
        "daily": ["weather_code", "temperature_2m_max","temperature_2m_min" ,"sunrise", "sunset"],
        # "forecast_days": 1,
        "temperature_unit": "fahrenheit",
    }   
    responses = openmeteo.weather_api(url, params = params)

    # just processing the first location as response might give multiple locations
    response = responses[0]
    return response

def hourly_forecast_df(response):
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["weather_code"] = hourly_weather_code
    hourly_dataframe_pd = pd.DataFrame(data = hourly_data)
    hourly_dataframe_pd["time_in_hour"] = hourly_dataframe_pd["date"].apply(lambda x: pd.to_datetime(x).to_pydatetime().strftime("%-I %p"))
    # for i in range(1, 5):
    #     print(f"{hourly_dataframe_pd['date'][i]} -> {hourly_dataframe_pd['temperature_2m'][i]}")
    #     print()
    #Only sending the next 23 hours
    return hourly_dataframe_pd.head(23).to_dict("list")

if __name__ == '__main__':
    response = get_weather_response(42.4,-71.05)
    print("Hourly---")
    hourly_forecast_df(response)
    print("Daily---")
