import sys
sys.path.append('/workspaces/Event-Extraction')
from allennlp.predictors.predictor import Predictor
from mongodb.config import db
from nltk.tokenize import sent_tokenize
import csv

collection = db['kashmir_news']

csvfile = open('outputs/event.csv', 'w')
csvwriter = csv.writer(csvfile) 
length = collection.count_documents({})
model_url = "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz"
predictor = Predictor.from_path(model_url)

for i,document in enumerate(collection.find()):
    print("----processing document {}/{}".format(i+1,length))
    try:
        description = document['description']
        prediction = predictor.predict(document=description)
        new_description = predictor.coref_resolved(description)

        sentences = sent_tokenize(new_description)
    
        for sentence in sentences:
                csvwriter.writerow([sentence])

    except Exception as e:
        print("error in writing sentence: {}".format(e))
csvfile.close()

     




