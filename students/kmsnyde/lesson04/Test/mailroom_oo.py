# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 10:17:33 2018

@author: HP-Home
"""

import json_save_dec as js
import json
import os


@js.json_save
class Donor:

    name = js.String()
    donations = js.List()

    def __init__(self, name, donations):
        self.name = name
        self.donations = donations

    @property
    def total_donations(self):
        return sum(self.donations)

    @property
    def num_of_gifts(self):
        return len(self.donations)

    def add_donation(self, donation):
        self.donations.append(donation)

    def save_data(self):
        data = self.to_json_compat()
        data = json.dumps(data)
        with open('{}.json'.format(self.name), 'w') as datafh:
            datafh.write(data)

    @classmethod
    def load_data(cls, donor_name):
        with open('{}'.format(donor_name), 'r') as ddatafh:
            ddata = ddatafh.read()
        ddata = json.loads(ddata)
        return cls.from_json_dict(ddata)


class Mailroom:

    def __init__(self, donors):
        self.donors = donors

    def save_donors(self):
        for donor in self.donors:
            donor.save_data()

    def load_donors(self):
        _donors = []
        donors_files = os.listdir('.')
        donors_names = [z for z in donors_files if z.split('.')[-1] == 'json']
        for donor in donors_names:
            _donors.append(Donor.load_data(donor))
        self.donors = _donors

    def add_donor(self, donor):
        self.donors.append(donor)

    def get_donor(self, given_donor):
        for donor in self.donors:
            if donor.name == given_donor:
                return donor

    def send_thankyou(self, donor_name):
        donor = self.get_donor(donor_name)
        return 'Thank you {} for your generous donation of {}'.format(
            donor.name, donor.total_donations
        )

    def all_donors(self):
        return [x.name for x in self.donors]

    def list_donors(self):
        return "\n".join(self.all_donors())

    def create_report(self):
        print('{:20} | {:15} | {:10} | {:15}'.format(
            'Donor Name', 'Total Given', 'Num Gifts', 'Average Gift'))
        print('-'*70)
        for donor in self.donors:
            print('{:20} | {:15} | {:10} | {:15}'.format(
                donor.name, donor.total_donations,
                donor.num_of_gifts,
                donor.total_donations / donor.num_of_gifts))

    def save_report(self):
        for donor in self.donors:
            with open(donor.name+'.txt', 'w') as donorfh:
                donorfh.write(self.send_thankyou(donor.name))