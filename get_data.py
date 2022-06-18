import requests
import pymongo
myclient = pymongo.MongoClient("mongodb+srv://admin:MSf587ncpLo41Ocl@cluster0.op8ul.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["news_data"]
collection = mydb["kashmir_news"]

parameters = {
    'access_key': 'feba328cc461b61f572f980f90669b6d',
    'date':'2022-03-1,2022-04-1',
    'countries':"in",
    'limit':'100',
    'categories':'general',
    'keywords' :'kashmir'
    }
response = requests.get('http://api.mediastack.com/v1/news',params=parameters)
json_response = response.json()

data = json_response['data']

x = collection.insert_many(data)