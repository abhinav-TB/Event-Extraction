from csv import DictReader, DictWriter
from os import system, replace
from os.path import relpath
from textwrap import dedent
from tempfile import NamedTemporaryFile

comparison_file_path = "outputs/comparison.csv"

with open(comparison_file_path, "r") as f, NamedTemporaryFile(
    mode="w", suffix=".csv", dir="outputs", delete=False
) as temp_file:
    reader = DictReader(f)
    if reader.fieldnames:
        twriter = DictWriter(temp_file, fieldnames=reader.fieldnames)
        twriter.writeheader()

        total = 0
        stanford_location_better = 0
        allen_location_better = 0
        stanford_date_better = 0
        heidal_date_better = 0

        skip = False

        for row in reader:
            if skip:
                twriter.writerow(row)
                continue

            try:
                if row["best_location"] == "" or row["best_date"] == "":

                    system("clear")
                    manual_tags = input(
                        dedent(
                            f"""
                    Event: {row["event"]}
                    Article Date: {row["article_date"]}

                    Stanford location: {row["stanford_location"]}
                    Allen location: {row["allen_location"]}
                    Stanford date: {row["stanford_date"]}
                    HeidalTime date: {row["heidal_date"]}

                    Input format:
                    <location> <date>

                    <location> is 0 for Stanford, 1 for Allen, 2 if both are correct and 3 if both are wrong
                    <date> is 0 for Stanford, 1 for HeidalTime, 2 if both are correct and 3 if both are wrong

                    Type input:
                    """
                        )
                    ).split(" ")

                    row["best_location"] = manual_tags[0]
                    row["best_date"] = manual_tags[1]

                    system("clear")

                if row["best_location"] == "0":
                    stanford_location_better += 1
                elif row["best_location"] == "1":
                    allen_location_better += 1
                elif row["best_location"] == "2":
                    stanford_location_better += 1
                    allen_location_better += 1

                if row["best_date"] == "0":
                    stanford_date_better += 1
                elif row["best_date"] == "1":
                    heidal_date_better += 1
                elif row["best_date"] == "2":
                    stanford_date_better += 1
                    heidal_date_better += 1

                total += 1

                twriter.writerow(row)

            except KeyboardInterrupt:
                system("clear")
                skip = True
                twriter.writerow(row)

        replace(src=relpath(temp_file.name), dst=comparison_file_path)

        print(
            dedent(
                f"""
        Stanford location better: {stanford_location_better}
        Allen location better: {allen_location_better}
        Stanford date better: {stanford_date_better}
        HeidalTime date better: {heidal_date_better}
        Total: {total}
        """
            )
        )
