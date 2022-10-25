from csv import DictReader, DictWriter
from datetime import datetime
from typing import Optional, Dict, List
from datatypes_timex_expression import Timex


csvfile = open("outputs/allen_heidal_time_loc_and_date_filled.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "news_id",
        "news_title",
        "event",
        "event_type",
        "url",
        "date_prediction",
        "location_prediction",
    ],
)
csvwriter.writeheader()


with open("outputs/tagged_events_raw_allen.csv", "r") as f:
    reader = DictReader(f)
    prev_token_date = False

    article_id_to_tags: Dict[str, Dict[str, str]] = {}

    for i, row in enumerate(reader):
        id = row["news_id"]
        event = row["event"]
        location_prediction = row["location_prediction"]
        date_prediction = row["date_prediction"]

        if id not in article_id_to_tags:
            article_id_to_tags[id] = {
                "location": location_prediction,
                "date": date_prediction,
            }
        else:
            if location_prediction != "":
                article_id_to_tags[id]["location"] = location_prediction
            if date_prediction is not None:
                article_id_to_tags[id]["date"] = str(date_prediction)

        if location_prediction == "" and id in article_id_to_tags:
            location_prediction = article_id_to_tags[id]["location"]

        if date_prediction is None and id in article_id_to_tags:
            date_prediction = article_id_to_tags[id]["date"]

        csvwriter.writerow(
            {
                "news_id": row["news_id"],
                "news_title": row["news_title"],
                "event": row["event"],
                "event_type": row["event_type"],
                "url": row["url"],
                "date_prediction": date_prediction,
                "location_prediction": location_prediction,
            }
        )
