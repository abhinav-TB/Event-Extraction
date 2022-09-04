from csv import DictReader, DictWriter

csvfile = open("outputs/village_directory.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "village",
        "district",
        "state",
    ],
)
csvwriter.writeheader()

with open("data/jammukashmir_villages.csv", "r") as f:
    reader = DictReader(f)

    for i, row in enumerate(reader):
        village = row["VILLAGE NAME"]
        district = row["DISTRICT NAME"]
        state = row["STATE NAME"]

        csvwriter.writerow(
            {
                "village": village,
                "district": district,
                "state": state,
            }
        )
