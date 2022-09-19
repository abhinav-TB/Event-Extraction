from csv import DictReader


class FullLocation:
    def __init__(self):
        self.village_dict = dict()
        self.district_dict = dict()
        self.state_set = set()
        self.populate()

    def populate(self):
        with open("outputs/village_directory.csv", "r") as f:
            reader = DictReader(f)

            for row in reader:
                village = row["village"]
                district = row["district"]
                state = row["state"]

                self.village_dict[village] = {
                    "village": village,
                    "district": district,
                    "state": state,
                }
                self.district_dict[district] = {
                    "village": None,
                    "district": district,
                    "state": state,
                }
                self.state_set.add(state)

    def get_location_village(self, village):
        return self.village_dict.get(village)

    def get_location_district(self, district):
        return self.district_dict.get(district)

    def is_location_state(self, state):
        return state in self.state_set

    def get_location(self, location):
        village_loc = self.get_location_village(location)
        if village_loc:
            return village_loc

        district_loc = self.get_location_district(location)
        if district_loc:
            return district_loc

        if self.is_location_state(location):
            return {"village": None, "district": None, "state": location}

        return {"village": None, "district": None, "state": None}
