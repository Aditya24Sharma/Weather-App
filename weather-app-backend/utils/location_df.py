import pandas as pd
import duckdb

#Description: Take zip code and returns info about that location after querying through the dataset
#return : dictionary (zip,type,primary_city,state,county,standard_timezone,place_timezone,area_codes,latitude,longitude)

def get_location_info(zip_code = 39406):
    location_df = duckdb.sql(f"""
        SELECT * FROM '../../location_dataset/Zip_codes_with_location.csv' as 'dataset'
        WHERE zip = {zip_code}
            """
    ).df()

    location_dict = location_df.to_dict('list')
    for key, values in location_dict.items():
        location_dict[key] = location_dict[key][0]

    # print(type(location_dict['zip']))
    return location_dict

if __name__ == '__main__':
    get_location_info()