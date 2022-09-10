from csv import DictReader, DictWriter
from stanza.server import CoreNLPClient

MAX_LENGTH = 1000

csvfile = open("outputs/tagged_events_raw_stanford.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "article_id",
        "article_title",
        "article_date",
        "event",
        "event_type",
        "location_prediction",
        "date_prediction_text",
        "date_prediction_value",
    ],
)
csvwriter.writeheader()

with CoreNLPClient(
    annotators=[
        "tokenize",
        "ssplit",
        "pos",
        "lemma",
        "ner",
        "parse",
        "depparse",
        "coref",
    ],
    timeout=3000000,
    memory="4G",
    be_quiet=False,
) as client:
    with open("outputs/events.csv", "r") as f:
        reader = DictReader(f)

        for i, row in enumerate(reader):
            event = row["event"]

            if len(event) > MAX_LENGTH:
                continue

            try:
                ann_sentence = client.annotate(event)
            except Exception as e:
                print(e)
                continue
            location = []
            date_text = ""
            date_value = ""

            prev_token_date = False
            prev_token_location = False

            for token in ann_sentence.sentence[0].token:
                if token.ner != "O":
                    if token.ner == "DATE":
                        if prev_token_date:
                            continue
                        else:
                            prev_token_date = True
                        print(f"Date found in event {i}: {token.timexValue.text}")
                        date_text = token.timexValue.text
                        date_value = (
                            token.timexValue.altValue
                            if token.timexValue.altValue
                            else token.timexValue.value
                        )

                    elif token.ner == "LOCATION":
                        if prev_token_location:
                            location[-1] += " " + token.value
                        else:
                            location.append(token.value)
                        prev_token_location = True
                        print(f"Location found in event {i}: {token.value}")
                    else:
                        prev_token_date = False
                        prev_token_location = False
                else:
                    prev_token_date = False
                    prev_token_location = False

            csvwriter.writerow(
                {
                    "article_id": row["article_id"],
                    "article_title": row["article_title"],
                    "article_date": row["article_date"],
                    "event": row["event"],
                    "event_type": row["event_type"],
                    "location_prediction": list(set(location))
                    if len(location) > 0
                    else None,
                    "date_prediction_text": date_text,
                    "date_prediction_value": date_value,
                }
            )

            if not client.is_alive():
                client.start()
