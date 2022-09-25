from os import system
from textwrap import dedent

from write_to_csv_with_memory import write_to_csv_with_memory

comparison_file_path = "outputs/comparison.csv"

total = 0
stanford_location_better = 0
allen_location_better = 0
stanford_date_better = 0
heidal_date_better = 0


def process_row(i, row):
    global total
    global stanford_location_better
    global allen_location_better
    global stanford_date_better
    global heidal_date_better

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

    return row


def after_effect():
    system("clear")
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


write_to_csv_with_memory(
    input_file_path=None,
    output_file_path="outputs/comparison.csv",
    fieldnames=None,
    process_row=process_row,
    after_effect=after_effect,
)
