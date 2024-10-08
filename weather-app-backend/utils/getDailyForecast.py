import pandas as pd

def getDailyForecast(response):
    # "daily": ["weather_code", "temperature_2m_max","temperature_2m_min" ,"sunrise", "sunset"],
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_data = {"date":pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["Max_Temp"] = daily_temperature_2m_max
    daily_data["Min_Temp"] = daily_temperature_2m_min
    daily_dataframe_pd = pd.DataFrame(data = daily_data)
    daily_dataframe_pd["weather_code"] = daily_dataframe_pd["weather_code"].apply(lambda x: str(int(x)))
    daily_dataframe_pd["Max_Temp"] = daily_dataframe_pd["Max_Temp"].apply(lambda x: round(x))
    daily_dataframe_pd["Min_Temp"] = daily_dataframe_pd["Min_Temp"].apply(lambda x: round(x))
    daily_dataframe_pd["Date"] = daily_dataframe_pd["date"].apply(lambda x: pd.to_datetime(x).to_pydatetime().strftime("%-m/%d"))
    daily_dataframe_pd["day_of_week"] = daily_dataframe_pd["date"].apply(lambda x: (pd.to_datetime(x).to_pydatetime().strftime("%A"))[:3])
    daily_dataframe_pd["image"] = daily_dataframe_pd["weather_code"].apply(lambda x: str(int(x))+'_day')
    #setting the first day to today
    daily_dataframe_pd.loc[0, "day_of_week"] = "Today"

    dict_daily_forecast = daily_dataframe_pd[['weather_code', 'Max_Temp', 'Min_Temp', 'Date', 'day_of_week','image']].set_index('Date').to_dict(orient='index')

    return dict_daily_forecast
    

