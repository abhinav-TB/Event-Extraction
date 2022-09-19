# check for relevant news and discard the rest
import nltk
import sys
sys.path.append("../")
from nltk.corpus import wordnet
from mongodb.config import db
nltk.download('omw-1.4')
collection = db["news"]

new_collection = db["category_news"]
# find synonyms of these words with wordnet
parent_words = ["kill","strike","murder","attack","protest","terror","suicide","rape","kidnap","crime","fight","curfew","molest","stone pelting","shoot","Violence","explosion"]#
key_words = {}

for word in parent_words:
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name() not in key_words:
               key_words[l.name()] = word

## discard news without the keywords
for i, document in enumerate(collection.find()):
    description = document["content"]
    words = nltk.word_tokenize(description)
    for word in words:
        if word in key_words:
            document['category'] = key_words[word]
            new_collection.insert_one(document)
            break   
           
