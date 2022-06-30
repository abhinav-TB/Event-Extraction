from spacy import load
from csv import DictReader

nlp = load("en_core_web_sm")

with open("outputs/events.csv", "r") as f:
    reader = DictReader(f)
    for row in reader:
        event = row["event"]
        doc = nlp(event)
        for ent in doc.ents:
            if ent.label_ == "DATE":
                print(ent.text)
        


# Process whole documents
text = (
    "When Sebastian Thrun started working on self-driving cars at "
    "Google in 2007, few people outside of the company took him "
    "seriously. “I can tell you very senior CEOs of major American "
    "car companies would shake my hand and turn away because I wasn’t "
    "worth talking to,” said Thrun, in an interview with Recode earlier "
    "this week."
)
doc = nlp(text)

for ent in doc.ents:
    if ent.label_ == "DATE":
        print(ent.text)
