
import json
import sys
sys.path.append("../")
from mongodb.config import db

news_collection = db["news"]

## bulk write documents from json file
with open("../data/news_kashmir_20July-31Aug19.json", "r") as f:
    news_data = json.load(f)

    # removing already existing mongodb ids
    for news in news_data:
        del news['_id']
    
    # inserting into the database
    news_collection.insert_many(news_data)
    print("Inserted {} news documents".format(len(news_data)))