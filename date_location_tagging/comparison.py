from csv import DictWriter, DictReader

csvfile = open("outputs/comparison.csv", "w")
csvwriter = DictWriter(
    csvfile,
    fieldnames=[
        "article_id",
        "event",
        "stanford_location",
        "allen_location",
        "stanford_date",
        "heidal_date",
        "actual_location",
        "actual_date",
    ],
)
csvwriter.writeheader()

ht_path = "outputs/heidal_Time.csv"
al_path = "outputs/tagged_events_raw_allen.csv"
st_path = "outputs/tagged_events_raw_stanford.csv"
st_resolved_path = "outputs/tagged_events_resolved.csv"

with open(ht_path, "r") as ht_f, open(al_path, "r") as al_f, open(
    st_path, "r"
) as st_f, open(st_resolved_path, "r") as st_r_f:
    ht_reader = DictReader(ht_f)
    al_reader = DictReader(al_f)
    st_reader = DictReader(st_f)
    st_r_reader = DictReader(st_r_f)
    ht_dates_predicted = 0
    st_dates_predicted = 0
    st_locations_predicted = 0
    al_locations_predicted = 0
    for ht_row, al_row, st_row, st_r_row in zip(
        ht_reader, al_reader, st_reader, st_r_reader
    ):
        ht_date_valid = ht_row["date_prediction"] != "[]"
        st_date_valid = st_row["date_prediction_text"] != ""
        st_location_valid = st_row["location_prediction"] != ""
        al_location_valid = al_row["location_prediction"] != ""
        if ht_date_valid or st_date_valid or st_location_valid or al_location_valid:
            if ht_date_valid:
                ht_dates_predicted += 1
            if st_date_valid:
                st_dates_predicted += 1
            if st_location_valid:
                st_locations_predicted += 1
            if al_location_valid:
                al_locations_predicted += 1
            csvwriter.writerow(
                {
                    "article_id": ht_row["article_id"],
                    "event": ht_row["event"],
                    "stanford_location": st_row["location_prediction"],
                    "allen_location": al_row["location_prediction"],
                    "stanford_date": st_r_row["date_prediction"],
                    "heidal_date": ht_row["date_prediction"],
                    "actual_location": "",
                    "actual_date": "",
                }
            )
    print(f"{ht_dates_predicted} predicted dates by Heidal Time")
    print(f"{st_dates_predicted} predicted dates by CoreNLP")
    print(f"{st_locations_predicted} predicted locations by CoreNLP")
    print(f"{al_locations_predicted} predicted locations by AllenNLP")
