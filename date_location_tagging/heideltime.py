from py_heideltime import py_heideltime
from csv import DictWriter, DictReader

csvfile = open("../outputs/heidal_Time.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "news_id",
        "news_title",
        "date_prediction",
        "event",
        "event_type",
        "url",
    ],
)
csvwriter.writeheader()

# read from a csvfile
with open("../outputs/events.csv", "r") as f:
    reader = DictReader(f)
    for i, row in enumerate(reader):
        print("----processing document {}".format(i + 1))
        results = py_heideltime(
            row["event"],
            language="english",
            date_granularity="day",
            document_type="news",
            document_creation_time=row["article_date"][:10],
        )
        csvwriter.writerow(
            {
                "news_id": row["news_id"],
                "news_title": row["article_title"],
                "event": row["event"],
                "date_prediction": results[0],
                "event_type": row["event_type"],
                "url": row["url"],
            }
        )
