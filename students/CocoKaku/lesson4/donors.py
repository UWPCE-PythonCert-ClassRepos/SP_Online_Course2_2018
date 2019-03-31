"""
updated Donors class for Python 220 Lesson 4 assignment (metaprogramming)
(1) added json_save decorator to Donor and Donors classes
(2) changed thank you letter to be from "Python 220 Class of 2019"
"""

from os import mkdir
from os.path import isdir
from functools import reduce
import json_save_zip.json_save.json_save_dec as js

@js.json_save
class Donor():
    """
    Donor class

    attributes:
        _name = name of donor
        _donations = list of donations

    methods:
        num_donations
        sum_donations
        avg_donation
        add_donation
        thank_you_letter
    """
    _name = js.String()
    _donations = js.List()

    def __init__(self, name, donation):
        self._name = name
        if isinstance(donation, list):
            self._donations = donation
        else:
            self._donations = [float(donation)]

    @property
    def name(self):
        return self._name

    @property
    def donations(self):
        return self._donations

    def num_donations(self):
        return len(self._donations)

    def sum_donations(self):
        return sum(self._donations)

    def avg_donation(self):
        return sum(self._donations) / len(self._donations)

    def add_donation(self, donation):
        self._donations.append(float(donation))

    def thank_you_letter(self):
        return f"Dear {self._name},\n" \
               f"Thank you very much for your generous donation of ${self._donations[-1]:,.2f}.\n" \
               f"Sincerely,\n" \
               f"PYTHON220 Class of 2019"

@js.json_save
class Donors():
    """
    Donors class

    inherits from:
    dict

    methods:
    list_donors
    add_donor
    add_donation
    thank_you_letter
    summary_report
    send_all_letters

    classmethods:
    get_second = returns second element in a sequence, used as key for sorting
    """
    db = js.Dict()
    def __init__(self, d=None):
        self.db = {}
        if d:
            for name, donations in d.items():
                self.db[name] = Donor(name, donations)

    def list_donors(self):
        return '\n'.join(['   '+name for name in self.db])

    def add_donor(self, donor):
        self.db[donor.name] = donor

    def add_donation(self, name, donation):
        if name in self.db:
            self.db[name].add_donation(donation)
        else:
            self.db[name] = Donor(name, donation)

    def thank_you_letter(self, donor):
        return self.db[donor].thank_you_letter()

    def summary_report(self):
        summary_list = [(d.name, d.sum_donations(), d.num_donations(), d.avg_donation())
                        for _, d in self.db.items()]
        summary_list.sort(key=Donors.get_second, reverse=True)
        report = "DONOR NAME             TOTAL DONATED   NUM DONATIONS   AVG DONATION\n"
        for (name, total, num, avg) in summary_list:
            report += f"{name:20s}   ${total:12,.2f} {num:3d}               ${avg:11,.2f}\n"
        return report

    def send_all_letters(self, dir_name):
        if not isdir(dir_name):
            mkdir(dir_name)
        for name in self.db:
            file_name = dir_name + '/' + name.replace(',', '').replace(' ', '_') + '.txt'
            with open(file_name, 'w') as f:
                f.write(self.db[name].thank_you_letter())

    @classmethod
    def get_second(cls, sequence):
        try:
            return sequence[1]
        except IndexError:
            return None

    @classmethod
    def challenge(cls, cur_db, factor, min_donation=None, max_donation=None):
        new_db = Donors()
        for d in cur_db.db.values():
            donations = d.donations
            if min_donation:
                donations = list(filter(lambda x: x >= min_donation, donations))
            if max_donation:
                donations = list(filter(lambda x: x <= max_donation, donations))
            if donations:
                new_db.add_donor(
                    Donor(d.name, list(map(lambda x: round(x * factor, 2), donations))))
        return new_db

    def total_value(self):
        total = 0
        for d in self.db.values():
            total += reduce(lambda x, y: x+y, d.donations)
        return total
