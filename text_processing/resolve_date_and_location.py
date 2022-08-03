from csv import DictReader, DictWriter
from datatypes_timex_expression import Timex
from pprint import pprint


csvfile = open("outputs/tagged_events_resolved.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "event",
        "location_prediction",
        "date_prediction",
    ],
)
csvwriter.writeheader()

with open("outputs/tagged_events_raw_stanford.csv", "r") as f:
    reader = DictReader(f)
    prev_token_date = False

    for i, row in enumerate(reader):
        event = row["event"]
        location_prediction = row["location_prediction"]
        date_prediction = ""

        if row["date_prediction_value"]:
            timex = Timex(row["date_prediction_value"])
            print(
                f"Date found in event: {i}, text: {row['date_prediction_text']}, value: {row['date_prediction_value']}"
            )
            pprint(vars(timex))

        csvwriter.writerow(
            {
                "event": event,
                "location_prediction": location_prediction,
                "date_prediction": date_prediction,
            }
        )
