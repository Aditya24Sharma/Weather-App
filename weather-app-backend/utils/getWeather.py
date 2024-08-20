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
        "current": ["temperature_2m", "apparent_temperature", "is_day", "precipitation", "rain"],
        "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "weather_code"],
        "daily": ["weather_code", "temperature_2m_max", "sunrise", "sunset"],
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
    # for i in range(1, 5):
    #     print(f"{hourly_dataframe_pd['date'][i]} -> {hourly_dataframe_pd['temperature_2m'][i]}")
    #     print()
    print(hourly_dataframe_pd.head(5))
    return hourly_dataframe_pd

def daily_forecast(response):
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_sunrise = daily.Variables(2).ValuesAsNumpy()
    daily_sunset = daily.Variables(3).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["sunrise"] = daily_sunrise
    daily_data["sunset"] = daily_sunset

    daily_dataframe = pd.DataFrame(data = daily_data)
    print(daily_dataframe.head(5))


if __name__ == '__main__':
    response = get_weather_response(42.4,-71.05)
    print("Hourly---")
    hourly_forecast_df(response)
    print("Daily---")
    daily_forecast(response)
