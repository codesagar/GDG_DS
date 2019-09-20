import json
import requests
import pandas
from bs4 import BeautifulSoup
import sys

querry_url = "https://www.olx.in/api/relevance/search?category=84&location=4058732"
# querry_url = "https://www.olx.in/api/relevance/search?category=84&facet_limit=1&location=4058732&location_facet_limit=1"

def get_data_from_url(url):
    r = requests.get(url)
    c = r.content

    soup = BeautifulSoup(c, 'html.parser')
    body = json.loads(soup.text)

    allCars = []

    # Extracting Features
    for car in body['data']:
        try:
            currentCar = {}
            currentCar['Price'] = car['price']['value']['raw']
            for meta_parameter in ['title','description','created_at']:
                if car[meta_parameter]:
                    currentCar[meta_parameter] = car[meta_parameter]
            for parameter in car['parameters']:
                if parameter['key'] == 'year':
                    currentCar["Year"] = parameter['value']
                elif parameter['key'] == 'petrol':
                    currentCar["fuel"] = parameter['value']
                elif parameter['key'] == 'mileage':
                    currentCar["Kms"] = parameter['value']
                elif parameter['key'] == 'model':
                    currentCar["model"] = parameter['value']
                elif parameter['key'] == 'make':
                    currentCar["make"] = parameter['value']
            currentCar["City"] = car['locations_resolved']['ADMIN_LEVEL_3_name']
            currentCar["Area"] = car['locations_resolved']['SUBLOCALITY_LEVEL_1_name']
            allCars.append(currentCar)

        # Error Logging
        except:
            print("Unexpected error for post", sys.exc_info()[0])

    # Check if we have next page
    nextPage = False
    if len(body['data']) > 0 and ('next_page_url' in body['metadata']):
        nextPage = True
    return [allCars, nextPage]

# Data to CSV
cumulativeCarData = []
make = ['mahindra','volkswagen','chevrolet','hyundai','cars-honda','maruti-suzuki','tata','ford','toyota','skoda','renault','nissan','mercedes-benz','bmw','audi']
for mk in make:
    print("Make =", mk)
    for i in range(50):
        url = querry_url + "&page=" + str(i) + "&make=" + mk
        dataFromFunction = get_data_from_url(url)
        cumulativeCarData += dataFromFunction[0]
        print("Page ",i+1, " completed")
        df = pandas.DataFrame(cumulativeCarData)
        df.to_csv("olx_data.csv", header=False, index=False)
        if not dataFromFunction[1]:
            break

