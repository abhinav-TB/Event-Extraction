from csv import DictReader, DictWriter
from location_dictionary import FullLocation


csvfile = open("outputs/final_tagged_events.csv", "w")
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


with open("outputs/tagged_events_resolved.csv", "r") as f:
    reader = DictReader(f)
    fu

    for i, row in enumerate(reader):
        id = row["article_id"]
        loc = row["location_prediction"]
        loc = loc[1:-1]
        print(f"after: {loc}")
        loc_items = loc.split(", ")
        loc_items = [i[1:-1] for i in loc_items]
        loc_items_full = []
        

        # csvwriter.writerow(
        #     {
        #         "article_id": row["article_id"],
        #         "event": event,
        #         "location_prediction": location_prediction,
        #         "date_prediction": date_prediction,
        #     }
        # )
