from os import system
from stanza.server import CoreNLPClient

from utils import write_to_csv_with_memory

MAX_LENGTH = 1000

input_file_path = "outputs/events.csv"
output_file_path = "outputs/tagged_events_raw_stanford.csv"

# Only doing location tagging with Stanford because HeidalTime is better at date tagging
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
    timeout=300000,
    memory="4G",
    be_quiet=True,
) as client:
    system("clear")

    def process_row(i, row):
        event = row["event"]

        if len(event) > MAX_LENGTH:
            return row

        try:
            ann_sentence = client.annotate(event)
        except Exception as e:
            print(e)
            return row

        location = []
        prev_token_location = False

        for token in ann_sentence.sentence[0].token:
            if token.ner != "O":
                if token.ner == "LOCATION":
                    if prev_token_location:
                        location[-1] += " " + token.value
                    else:
                        location.append(token.value)
                    prev_token_location = True

                    system("clear")
                    print(f"Locations found in row {i}: {location}")
                else:
                    prev_token_location = False
            else:
                prev_token_location = False

        row["location_prediction"] = list(set(location)) if len(location) > 0 else None

        system("clear")
        print(f"Row {i} done")

        return row

    def after_effect():
        system("clear")
        print(f"Updated {output_file_path}")

    write_to_csv_with_memory(
        input_file_path=input_file_path,
        output_file_path=output_file_path,
        fieldnames=[
            "news_id",
            "article_title",
            "article_date",
            "event",
            "event_type",
            "url",
            "location_prediction",
        ],
        process_row=process_row,
        after_effect=after_effect,
    )
