from flask import Flask, jsonify 
import requests
from getWeather import get_current_weather

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
    currentWeather = get_current_weather()
    currentTemperature = currentWeather.Variables(0).Value()
    return f'<p>The current weather is {currentTemperature:.2f}</p>'

@app.route('/weather', methods = ['GET'])
def get_weather():
    link = 'https://open-meteo.com/en/docs#latitude=42.3584&longitude=-71.0598&current=temperature_2m,apparent_temperature,is_day,precipitation,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum&temperature_unit=fahrenheit'
    response = requests.get(link)
    print(response.content)


if __name__== '__main__':
    app.run(debug = True)
