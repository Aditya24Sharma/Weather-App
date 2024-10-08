import pandas as pd
import duckdb
import os

#Description: Take zip code and returns info about that location after querying through the dataset
#return : dictionary (zip,type,primary_city,state,county,standard_timezone,place_timezone,area_codes,latitude,longitude)

def get_location_info(zip_code = 39406):
    file_path = 'Zip_codes_with_location.csv'
    abs_file_path = os.path.normpath(file_path)
    query = f"""
    SELECT * FROM '{abs_file_path}' as 'dataset'   
    WHERE zip = {zip_code}
        """
    location_df = duckdb.sql(query).df()
    location_dict = location_df.to_dict('list')
    for key, values in location_dict.items():
        try:
            location_dict[key] = location_dict[key][0]
        except:
            #return the default zipcode if the zipcode doesn't exist
            get_location_info()
            

    # print(location_dict['county'])
    return location_dict

def get_image(isday, weather_code):
    print(f"Weather Code: {weather_code}, is Day: {isday}")

if __name__ == '__main__':
    get_location_info()