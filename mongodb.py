import pymongo
myclient = pymongo.MongoClient("mongodb+srv://admin:MSf587ncpLo41Ocl@cluster0.op8ul.mongodb.net/?retryWrites=true&w=majority")
db = myclient["news_data_test"]
