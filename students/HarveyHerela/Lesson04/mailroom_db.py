import json_save.json_save.json_save.json_save_dec as js


class Donor:
    def __init__(self, firstname, lastname, donations=[]):
        self.name = (firstname, lastname)
        self.donations = donations

    def add_donation(self, amount):
        self.donations.append(amount)

    def get_donations(self):
        return self.donations

    def get_key(self):
        return self.name

    def get_name(self):
        return "{0} {1}".format(*self.name)


@js.json_save
class DonorCollection:

    donors = js.Dict()

    def __init__(self):
        self.donors.clear()

    def add_donor(self, donor, donations=[]):
        # Donor is a tuple: (first name, last name)
        # If donor already exists don't do anything
        if donor not in self.donors:
            self.donors[donor] = donations

    def get_donors(self):
        # Generate a list of donors, return one donor at a time
        for name, donations in self.donors.items():
            yield Donor(name[0], name[1], donations)

    def add_donation(self, firstname, lastname, amount):
        donor = (firstname, lastname)
        if donor not in self.donors:
            self.donors[donor] = []
        self.donors[donor].append(amount)

    def get_donations(self, firstname, lastname):
        donor = (firstname, lastname)
        return self.donors.get(donor, [])

    def load_db(self, other_db):
        # Overwrites this db with the data from the passed-in db
        self.donors.clear()
        for donor in other_db.get_donors():
            self.add_donor(donor.get_key(), donor.get_donations())
