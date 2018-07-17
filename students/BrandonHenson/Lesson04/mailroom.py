# Brandon Henson
# Python 220
# Lesson 4
# 7-17-18
# !/usr/bin/env python3

import json
from json_save_dec import json_save
from saveables import String, List


@json_save
class Donor():

    name = String()
    donations = List()

    def __init__(self, name, donations=[]):
        self.name = name
        self.donations = []
        for donation in donations:
            self.donations.append(donation)

    def new_donation(self, amount):
        self.donations.append(amount)

    def write_note(self, current_donation=0):
        note = ["Dear {},\n".format(self.name),
                '\nThank you for your generous donations \
totaling ${:,}.'.format(self.total_donated),
                "\nThe money will be put to good use."
                "\n\nSincerely, \n                -The Team"]
        if current_donation > 0:
            curr = ("This donation of ${:,} "
                    "really helps.".format(current_donation))
            note.insert(2, curr)
        return "".join(note)

    @property
    def total_donated(self):
        return sum(self.donations)

    @property
    def number_of_donations(self):
        return len(self.donations)

    @property
    def average_donation(self):
        return sum(self.donations) / len(self.donations)

    def __str__(self):
        return "{:17} ${:14,.2f}{:13} ${:13,.2f}".format\
            (self.name, self.total_donated, self.number_of_donations,
                self.average_donation)

    def __repr__(self):
        return "Donor(\'{}\', {})".format(self.name, self.donations)

    def __lt__(self, other):
        return self.total_donated < other.total_donated

    def __gt__(self, other):
        return self.total_donated > other.total_donated

    def __eq__(self, other):
        return self.total_donated == other.total_donated

    def __ne__(self, other):
        return self.total_donated != other.total_donated


@json_save
class Donor_list():

    donor_dictionary = List()

    def __init__(self, *args):
        self.donor_dictionary = []
        for arg in args:
            self.donor_dictionary.append(arg)

    def add_donor(self, *args):
        for arg in args:
            self.donor_dictionary.append(arg)

    def check_donor(self, name):
        donor_exists = False
        for donor in self.donor_dictionary:
            if name == donor.name:
                donor_exists = True
        return donor_exists

    def get_donor(self, name):
        for donor in self.donor_dictionary:
            if name == donor.name:
                return donor

    def sort_donors(self):
        return sorted(self.donor_dictionary, reverse=True)

    def donor_report(self):
        print("\n")
        print("Donor Name       |  Total Given  |  Num Gifts  |  Average Gift")
        for donor in self.sort_donors():
            print(donor)

    def save(self, file_name, info):
        name = "{}.json".format(file_name)
        with open(name, 'w') as f:
            f.write(info)
        print("saved")

    def __iter__(self):
        return self

    def __str__(self):
        return "\n".join(donor.name for donor in self.donor_dictionary)
