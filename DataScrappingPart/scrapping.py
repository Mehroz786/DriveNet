### This file contains the web-scrapping script

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs4
import time  # Add this import

## list of cars we wanna scrap
list_of_famous_cars = ['bmw-3-series','audi-a4','audi-a3']


#list_of_famous_cars = ['sportage']

## empty list to store the data
car_name = []
car_brand = []
price = []
engine_capacity = []
body_type = []
model_Year=[]
millage = []
fuel_type = []
transmission = []
city_registered = []
body_color = []


def request_function(url):
    req = requests.get(url).text
    soup = bs4(req, features="html.parser")
    return soup


def scrap_function():
    print('Loading Data ',end='')
    for car in list_of_famous_cars:
        for page in range(1,20):
            
            url = ' https://www.pakwheels.com/used-cars/search/-/?q='+car+'&page='+str(page)
            print(url)
            s1 = request_function(url)
            ads_link = ['https://www.pakwheels.com'+a.get('href') for a in s1.find_all('a',class_='car-name ad-detail-path')]
            for adlink in ads_link:
                print(adlink)


                s2 = request_function(adlink)

                car_name.append(s2.find('div',class_ = 'well').find_next('h1').text.strip().split()[1])

                car_brand.append((s2.find('div',class_ = 'well').find_next('h1').text.strip().split()[0]))

                model_Year.append(s2.find('span', class_ = 'engine-icon year').find_next().text.strip()
                                  if s2.find( 'span', class_='engine-icon year') else 'N/A')

                millage.append(s2.find('span', class_='engine-icon millage').find_next().text.strip())

                fuel_type.append(s2.find('span', class_='engine-icon type').find_next().text.strip())

                transmission.append(s2.find('span', class_='engine-icon transmission').find_next().text.strip())


                city_registered.append(s2.find('li', string='Registered In').find_next('li').get_text(strip=True))

                body_color.append(s2.find('li', string='Color').find_next('li').get_text(strip=True))

                engine_capacity.append(s2.find('li', string='Engine Capacity').find_next('li').get_text(strip=True)
                                       if s2.find('li',string='Engine Capacity') else s2.find(
                    'li', string='Battery Capacity').find_next('li').get_text)

                body_type.append(s2.find('li', string='Body Type').find_next('li').find('a').get_text()
                                 if s2.find('li', string='Body Type').find_next('li').find('a') else 'N/A')

                price.append(s2.find('strong',class_ = 'generic-green').text)


def converting_to_csv():
    start_time = time.time()
    scrap_function()
    print('Converting to DataFrame')
    df = pd.DataFrame({'Car_Name':car_name,'Car_Brand':car_brand,'Engine Capacity':engine_capacity,'Category':body_type,
                       "model Year":model_Year,'Milage':millage,'Fuel Type':fuel_type,'Transmission':transmission,
                       'City Registered':city_registered,'Price':price})

    print('Saving to CSV with Name --- > FYP DataSet',df.to_csv('FYP DataSet3.csv'))
    end_time = time.time()  # Record the end time
    runtime = end_time - start_time  # Calculate the runtime
    print(df)
    print("Run Time is ",runtime)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
        converting_to_csv()



