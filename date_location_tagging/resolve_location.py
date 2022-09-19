from csv import DictReader, DictWriter
from location_dictionary import FullLocation


def resolve_location(in_file, out_file):
    csvfile = open(out_file, "w")
    csvwriter = DictWriter(
        csvfile,
        fieldnames=[
            "news_id",
            "article_title",
            "article_date",
            "event",
            "location_prediction",
            "village",
            "district",
            "state",
            "date_prediction",
            "event_type",
            "url",
        ],
    )
    csvwriter.writeheader()

    with open(in_file, "r") as f:
        reader = DictReader(f)
        full_loc_helper = FullLocation()

        for i, row in enumerate(reader):
            loc = row["location_prediction"]
            loc = loc[1:-1]
            loc_items = loc.split(", ")
            loc_items = [i[1:-1] for i in loc_items]

            # TODO: Use all the locations later
            loc = loc_items[0]
            full_loc = full_loc_helper.get_location(loc)
            print("Location: ", loc)
            print("Full Location: ", full_loc)

            csvwriter.writerow(
                {
                    "news_id": row["news_id"],
                    "article_title": row["article_title"],
                    "article_date": row["article_date"],
                    "event": row["event"],
                    "location_prediction": loc,
                    "village": full_loc["village"],
                    "district": full_loc["district"],
                    "state": full_loc["state"],
                    "date_prediction": row["date_prediction"],
                    "event_type": row["event_type"],
                    "url": row["url"],
                }
            )


# resolve_location(
#     in_file="outputs/tagged_events_resolved.csv",
#     out_file="outputs/final_tagged_events.csv",
# )

resolve_location(
    in_file="outputs/tagged_events_raw_allen.csv",
    out_file="outputs/tagged_events_location_resolved_allen.csv",
)
