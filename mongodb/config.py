# mongo DB setup
import pymongo
import os
import dotenv

dotenv.load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

myclient = pymongo.MongoClient(MONGODB_URL)
db = myclient["news_data_test"]
