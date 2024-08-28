import pandas as pd

def getHourlyForecast(response):
    #"hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "weather_code"]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime((hourly.Time() + response.UtcOffsetSeconds()), unit = "s", utc = True),
        end = pd.to_datetime((hourly.TimeEnd() + response.UtcOffsetSeconds()), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature"] = hourly_temperature_2m
    hourly_data["apparent_temp"] = hourly_apparent_temperature
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["weather_code"] = hourly_weather_code
    hourly_dataframe_pd = pd.DataFrame(data = hourly_data)
    hourly_dataframe_pd["time_in_12hour"] = hourly_dataframe_pd["date"].apply(lambda x: pd.to_datetime(x).to_pydatetime().strftime("%-I"))
    hourly_dataframe_pd["AM_PM"] = hourly_dataframe_pd["date"].apply(lambda x: pd.to_datetime(x).to_pydatetime().strftime("%p"))
    hourly_dataframe_pd["time_in_24hour"] = hourly_dataframe_pd["date"].apply(lambda x: pd.to_datetime(x).to_pydatetime().strftime("%H"))
    hourly_dataframe_pd['temperature'] = hourly_dataframe_pd['temperature'].apply(lambda x: round(x))
    hourly_dataframe_pd['apparent_temp'] = hourly_dataframe_pd['apparent_temp'].apply(lambda x: round(x))
    hourly_dataframe_pd['weather_code'] = hourly_dataframe_pd['weather_code'].apply(lambda x: x)
    hourly_dataframe_pd['image'] = hourly_dataframe_pd["weather_code"].apply(lambda x: str(int(x))+('_day'))
    #only sending the hourly data for the hour of that day
    hourly_dict = hourly_dataframe_pd.head(24).set_index('time_in_24hour').to_dict(orient='index')
    return hourly_dict
