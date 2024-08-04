import json
import pandas as pd
import requests

# description: Saves the image for the given image link
# code: weather codes {0: sunny, 3: Cloudy, ....}
# time: time of the day (day or night) 
def save_img(img_url, code, time):
    img = requests.get(img_url).content
    file_path = f'{code}_{time}.png'
    with open(file_path, 'wb') as handler:
        handler.write(img)



with open('../weather_codes.json') as f:
    data = json.load(f)
    df = pd.DataFrame(columns = ['Code', 'Day_description', 'Day_img', 'Night_description', 'Night_img'])
    keys = list(data.keys())
    for key in keys:
        code = key
        # print(data[code]['day']["description"])
        Day_des = data[code]['day']["description"]
        Day_img = data[code]['day']['image']
        Night_des = data[code]['night']['description']
        Night_img = data[code]['night']['image']
        save_img(Day_img, code, 'day')
        save_img(Night_img, code, 'night')
        length = len(df)
        df.loc[length] = [code, Day_des, Day_img, Night_des, Night_img]
        

    print(df[df['Code'] == '1'])

