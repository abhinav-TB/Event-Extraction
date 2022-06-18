## program to collect news data from mediastack
import requests
from mongodb import db
news_collection = db["kashmir_news"]

def leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

def days_in_month(month, year):
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    if month == 2:
        if leap_year(year):
            return 29
        return 28
    return 30


def get_parameters(month, year):
    end_day = str(days_in_month(month, year))
    month = "0"+str(month) if month < 10 else str(month)
    year = str(year)
    parameters = {
        'access_key': 'feba328cc461b61f572f980f90669b6d',
        'date':f'{year}-{month}-1,{year}-{month}-{end_day}',
        'countries':"in",
        'limit':'100',
        'categories':'general',
        'keywords' :'kashmir'
        }
    return parameters


### get data for 6 months

for year in [2022]:
    for i in range(1,7):
        print("---processing month {} year {}---".format(i,year))
        parameters = get_parameters(i, year)
        print(parameters["date"])
        try:
            response = requests.get('http://api.mediastack.com/v1/news',params=parameters)
            json_response = response.json()
            data = json_response['data']
            print("articles_found",len(data))
            if len(data) > 0:
                x = news_collection.insert_many(data)
        
        except Exception as e:
            print("error",e)

