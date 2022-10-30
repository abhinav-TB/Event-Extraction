from csv import DictWriter, DictReader

csvfile = open(
    "outputs/allen_heidal_time_loc_and_date_filled_resolved_and_dropped_and_date_filled.csv",
    "w",
)
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "news_id",
        "news_title",
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

heidal_path = "outputs/allen_heidal_time_loc_and_date_filled_resolved_and_dropped.csv"
orig_path = "outputs/events.csv"

with open(heidal_path, "r") as ht_f, open(orig_path, "r") as o_f:
    ht_reader = DictReader(ht_f)
    o_reader = DictReader(o_f)

    for ht_row in ht_reader:
        if ht_row["date_prediction"] == "[]":
            for o_row in o_reader:
                if ht_row["event"] == o_row["event"]:
                    csvwriter.writerow(
                        {
                            "news_id": ht_row["news_id"],
                            "news_title": ht_row["news_title"],
                            "event": ht_row["event"],
                            "location_prediction": ht_row["location_prediction"],
                            "village": ht_row["village"],
                            "district": ht_row["district"],
                            "state": ht_row["state"],
                            "date_prediction": o_row["article_date"],
                            "event_type": ht_row["event_type"],
                            "url": ht_row["url"],
                        }
                    )
                    break
