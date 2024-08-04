from flask import Flask, jsonify 
import requests
from getWeather import get_weather_response, hourly_forecast_df

#creating an instance of the Flask class '__name__' so that Flask knows where to look for resources such as template and static files
app = Flask(__name__)

#the decorator registers the function with the given URL
# "latitude": latitude,
#     "longitude": longitude,
#     "current": ["temperature_2m", "apparent_temperature", "is_day", "precipitation", "weather_code"],
#     "hourly": "temperature_2m",
#     "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "precipitation_sum"],
#     "temperature_unit": "fahrenheit"
# } 
@app.route('/')
def home():
    response = get_weather_response(42.4,-71.05)
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_is_day = current.Variables(2).Value()
    current_precipitation = current.Variables(3).Value()
    current_weather_code = current.Variables(4).Value()

    print(f"Current time {current.Time()}")
    print(f"Current temperature_2m {current_temperature_2m}")
    print(f"Current apparent_temperature {current_apparent_temperature}")
    print(f"Current is_day {current_is_day}")
    print(f"Current precipitation {current_precipitation}")
    print(f"Current weather_code {current_weather_code}")

    return f'<p>The current weather is {current_temperature_2m:.2f}</p>'

@app.route('/hourly')
def hourly_weather():
    response = get_weather_response(42.4,-71.05)
    hourly_forecast = hourly_forecast_df(response)
    output = '<p>'
    for i in range(1, 5):
        output += f"<p>{hourly_forecast['date'][i]} -> {hourly_forecast['temperature_2m'][i]}" + '</p>' 

    return output

if __name__== '__main__':
    app.run(debug = True)
