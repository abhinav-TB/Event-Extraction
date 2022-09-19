from csv import DictReader, DictWriter
from allennlp_models import pretrained

ner_predictor = pretrained.load_predictor("tagging-fine-grained-transformer-crf-tagger")

csvfile = open("outputs/tagged_events_raw_allen.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "news_id",
        "article_title",
        "article_date",
        "event",
        "location_prediction",
        "date_prediction",
        "event_type",
        "url",
    ],
)
csvwriter.writeheader()

with open("outputs/events.csv", "r") as f:
    reader = DictReader(f)
    for i, row in enumerate(reader):
        event = row["event"]
        prediction = ner_predictor.predict(sentence=event)
        words = prediction["words"]
        tags = prediction["tags"]
        date = ""
        location = []

        last_word_was_date = False
        last_word_was_location = False

        for word, tag in zip(words, tags):
            if tag != "O":
                if tag.split("-")[1] == "DATE":
                    if last_word_was_date:
                        date += f" {word}"
                    else:
                        date = word
                    last_word_was_date = True
                    print(f"Date found in event {i}: {date}")
                elif tag.split("-")[1] == "GPE":
                    if last_word_was_location:
                        location[-1] += " " + word
                    else:
                        location.append(word)
                    last_word_was_location = True
                    print(f"Locations found in event {i}: {location}")
                else:
                    last_word_was_date = False
                    last_word_was_location = False
            else:
                last_word_was_date = False
                last_word_was_location = False
        csvwriter.writerow(
            {
                "news_id": row["news_id"],
                "article_title": row["article_title"],
                "article_date": row["article_date"],
                "event": row["event"],
                "location_prediction": list(set(location))
                if len(location) > 0
                else None,
                "date_prediction": date,
                "event_type": row["event_type"],
                "url": row["url"],
            }
        )
