from flask import Flask,redirect, url_for, request
from utils import get_weather_response, hourly_forecast_df, get_location_info, current_time, get_image

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
def redirect_to_home():
    return redirect(url_for('home'))

@app.route('/home', methods = ['GET'])
def home():
    zip_code = request.args.get('zipcode') or 39406
    print(zip_code)
    # zip_code = int('1010')
    location_info = get_location_info(zip_code)
    longitude = location_info['longitude']
    latitude = location_info['latitude']
    timezone = location_info['standard_timezone']
    locationTime = current_time(location_info['place_timezone'])
    city_name = location_info['primary_city']
    county = location_info['county']
    state = location_info['state']

    response = get_weather_response(latitude, longitude)
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_apparent_temperature = current.Variables(1).Value()
    current_is_day = current.Variables(2).Value()
    current_precipitation = current.Variables(3).Value()
    current_weather_code = current.Variables(4).Value()
    
    day_night = ("day" if current_is_day else "night")
    
    # print(f"Current time {current.Time()}")
    # print(f"Current temperature_2m {current_temperature_2m}")
    # print(f"Current apparent_temperature {current_apparent_temperature}")
    # print(f"Current is_day {current_is_day}")
    # print(f"Current precipitation {current_precipitation}")
    # print(f"Current weather_code {current_weather_code}")

    # return f'<p>The current weather is {current_temperature_2m:.2f}</p>'
    return {"current_temp": int(current_temperature_2m),
            "time": str(locationTime),
            "primary_city": city_name,
            "state": state,
            "county": county,
            "zip_code": zip_code,
            "image": f'{int(current_weather_code)}_{day_night}'}


@app.route('/hourly')
def hourly_weather():
    response = get_weather_response(42.4,-71.05)
    hourly_forecast = hourly_forecast_df(response)
    output = '<p>'
    for i in range(1, 5):
        output += f"<p>{hourly_forecast['date'][i]} -> {hourly_forecast['temperature_2m'][i]}" + '</p>' 

    # return output
    return {'first_hour': int(hourly_forecast['temperature_2m'][1])}


if __name__== '__main__':
    app.run(debug = True)
