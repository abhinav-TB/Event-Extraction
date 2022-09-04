import sys

sys.path.append("../")
from allennlp.predictors.predictor import Predictor
from allennlp_models.coref.predictors.coref import CorefPredictor
from mongodb.config import db
from nltk.tokenize import sent_tokenize
from csv import DictWriter

collection = db["news"]

csvfile = open("../outputs/events.csv", "w")
csvwriter = DictWriter(
    csvfile, fieldnames=["article_id", "article_title", "article_date", "event"]
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

        new_description = predictor.coref_resolved(description)
        sentences = sent_tokenize(new_description)

        for sentence in sentences:
            csvwriter.writerow(
                {
                    "article_id": i,
                    "article_title": title,
                    "article_date": article_date,
                    "event": sentence,
                }
            )

    except Exception as e:
        print("error in writing sentence: {}".format(e))
csvfile.close()
