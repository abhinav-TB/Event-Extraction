from csv import DictReader, DictWriter
from datetime import datetime
from typing import Optional, Dict, List
from datatypes_timex_expression import Timex


csvfile = open("outputs/tagged_events_resolved.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "article_id",
        "event",
        "location_prediction",
        "date_prediction",
    ],
)
csvwriter.writeheader()


def resolve_datetime(
    date_text: str, date_value: str, article_datetime: str
) -> Optional[datetime]:
    article_date = datetime.strptime(article_datetime.split("T")[0], "%Y-%m-%d")

    # TODO: text like the weekend, this summer, Wednesday, spring, etc. not handled

    # TODO: Yesterday, Tomorrow, etc. not handled
    if date_text == "now" or date_text == "today":
        return article_date

    # Things like "once", "recently", etc.
    if date_value == "PAST_REF":
        return None

    timex = Timex(date_value)

    # TODO: setting 1 as the default when day and month are not specified
    if timex.year is not None:
        return datetime(timex.year, int(timex.month or 1), int(timex.day_of_month or 1))

    if timex.month is not None:
        return datetime(article_date.year, timex.month, int(timex.day_of_month or 1))

    if timex.day_of_month is not None:
        return datetime(article_date.year, article_date.month, timex.day_of_month)


with open("outputs/tagged_events_raw_stanford.csv", "r") as f:
    reader = DictReader(f)
    prev_token_date = False

    article_id_to_tags: Dict[str, Dict[str, str]] = {}

    for i, row in enumerate(reader):
        id = row["article_id"]
        event = row["event"]
        location_prediction = row["location_prediction"]
        resolved_datetime = resolve_datetime(
            row["date_prediction_text"],
            row["date_prediction_value"],
            row["article_date"],
        )
        date_prediction = resolved_datetime.date() if resolved_datetime else None

        if id not in article_id_to_tags and (
            location_prediction != "[]" or date_prediction is not None
        ):
            article_id_to_tags[id] = {
                "location": location_prediction if location_prediction != "[]" else "",
                "date": str(date_prediction) if date_prediction else "",
            }
        else:
            if location_prediction != "[]":
                article_id_to_tags[id]["location"] = location_prediction
            if date_prediction is not None:
                article_id_to_tags[id]["date"] = str(date_prediction)

        if location_prediction == "[]" and id in article_id_to_tags:
            location_prediction = article_id_to_tags[id]["location"]

        if date_prediction is None and id in article_id_to_tags:
            date_prediction = article_id_to_tags[id]["date"]

        csvwriter.writerow(
            {
                "article_id": row["article_id"],
                "event": event,
                "location_prediction": location_prediction,
                "date_prediction": date_prediction,
            }
        )
