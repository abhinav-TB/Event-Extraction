from csv import DictReader

class Village:
    def __init__(self):
        self.village_dict = dict()
        self.district_dict = dict()
        self.populate()

    def populate(self):
        with open("outputs/village_directory.csv", "r") as f:
            reader = DictReader(f)

            for i, row in enumerate(reader):
                village = row["village"]
                district = row["district"]
                state = row["state"]

                self.village_dict[village] = f"{village}, {district}, {state}"
                self.district_dict[district] = f"{district}, {state}"

    def get_location_village(self, village):
        return self.village_dict.get(village)

    def get_location_district(self, district):
        return self.district_dict.get(district)

