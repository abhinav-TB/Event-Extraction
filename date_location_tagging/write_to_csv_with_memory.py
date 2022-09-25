from csv import DictReader, DictWriter
from os import replace
from os.path import relpath, isfile
from tempfile import NamedTemporaryFile
from typing import Callable, Any


def write_to_csv_with_memory(
    input_file_path: str | None,
    output_file_path: str,
    fieldnames: list[str] | None,
    process_row: Callable[
        [int, dict[str | Any, str | Any]], dict[str | Any, str | Any]
    ],
    after_effect: Callable[[], None] | None = None,
) -> None:
    """
    Write to a CSV file, while keeping a memory of the previous state of the file.
    If the CSV file doesn't exist, it will be created with the same data as the input file but with missing fields set to None.
    If input_file_path and fieldnames are None, it's assumed that the CSV file already exists.
    From process_row, return the row argument unchanged to skip that row.

    :param input_file_path: Path to the input CSV file
    :param output_file_path: The path to the CSV file to write to.
    :param fieldnames: The fieldnames of the output CSV file.
    :param process_row: A function that takes a row_index and row as input and returns a row as output.
    :param after_effect: A function that is called after the CSV file has been written to.
    :return: None
    """

    # Create file if it doesn't exist
    if (
        not isfile(output_file_path)
        and input_file_path != None
        and isfile(input_file_path)
        and fieldnames != None
    ):
        csvfile = open(output_file_path, "w")
        csvwriter = DictWriter(
            csvfile,
            fieldnames=fieldnames,
        )
        csvwriter.writeheader()

        with open(input_file_path, "r") as f:
            reader = DictReader(f)

            for row in reader:
                new_row = {}

                for fieldname in fieldnames:
                    if fieldname in row.keys():
                        new_row[fieldname] = row[fieldname]
                    else:
                        new_row[fieldname] = None

                csvwriter.writerow(new_row)

    # Write to output file
    with open(output_file_path, "r") as f, NamedTemporaryFile(
        mode="w", suffix=".csv", dir="outputs", delete=False
    ) as temp_f:
        reader = DictReader(f)

        if reader.fieldnames:
            twriter = DictWriter(temp_f, fieldnames=reader.fieldnames)
            twriter.writeheader()

            skip = False

            for i, row in enumerate(reader):
                if skip:
                    twriter.writerow(row)
                    continue

                try:
                    twriter.writerow(process_row(i, row))

                except KeyboardInterrupt:
                    skip = True
                    twriter.writerow(row)

            replace(src=relpath(temp_f.name), dst=output_file_path)

            if after_effect:
                after_effect()
