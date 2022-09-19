import sys
from unicodedata import category

sys.path.append("../")
from allennlp.predictors.predictor import Predictor
from allennlp_models.coref.predictors.coref import CorefPredictor
from mongodb.config import db
from nltk.tokenize import sent_tokenize
from csv import DictWriter

collection = db["category_news"]

csvfile = open("../outputs/events.csv", "w")
csvwriter = DictWriter(
    csvfile, fieldnames=["news_id", "article_title", "article_date", "event","event_type","url"]
)
csvwriter.writeheader()
length = collection.count_documents({})
model_url = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz"
predictor = Predictor.from_path(model_url)

for i, document in enumerate(collection.find()):
    print("----processing document {}/{}".format(i + 1, length))
    try:
        title = document["title"]
        description = document["content"]
        article_date = document["publishAt"]["$date"]
        category = document["category"]
        url = document["url"]
        news_id = document["_id"]
        new_description = predictor.coref_resolved(description)
        sentences = sent_tokenize(new_description)

        for sentence in sentences:
            csvwriter.writerow(
                {
                    "news_id": news_id,
                    "article_title": title,
                    "event": sentence,
                    "article_date": article_date,
                    "url": url,
                    "event_type": category,
                }
            )
            break
    except Exception as e:
        print("error in writing sentence: {}".format(e))
             
csvfile.close()
