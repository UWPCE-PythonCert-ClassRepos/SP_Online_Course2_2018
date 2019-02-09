#!/usr/bin/env python3

"""
A class-based system for managing donor information
"""



#@js.json_save
class Donor_obj():

#    first_name = js.String()
#    last_name = js.String()
#    donations = js.List()

    def __init__(self, donor_name, amount):
        self.donor_name = donor_name
        if type(amount) is list:
            self.donations = amount
        else:
            self.donations = [amount]

    @property
    def total(self):
        return sum(self.donations)

    @property
    def count(self):
        return len(self.donations)

    @property
    def average(self):
        if self.count == 0:
            return 0
        else:
            return self.total/self.count

    def __lt__(self, other):
        return self.total < other.total

    def __le__(self, other):
        return self.total <= other.total

    def __eq__(self, other):
        return self.total == other.total

    def __ge__(self, other):
        return self.total >= other.total

    def __gt__(self, other):
        return self.total > other.total

    def __ne__(self, other):
        return self.total != other.total


class DonorCollection():

    def __init__(self, donors=None):
        self.donorlist = donors

    def add_donor(self, first, last, amount):
        if self.donorlist is None:
            self.donorlist = [Donor(first, last, amount)]
        else:
            self.donorlist.append(Donor(first, last, amount))

    def load_donors(self, filename='donor_list.txt'):
        with open(filename, 'r') as f:
            for line in f:
                load = line.split(';')
                amount = [float(_) for _ in load[2].split(',')]
                self.add_donor(load[0],load[1],amount)

#    def load_donors(self, filename='donor_list.json'):
#        with open(filename, 'r') as f:
#            datastore = json.load(f)
#        for entry in datastore:
#            if self.donorlist is None:
#                self.donorlist = [Donor.from_json_dict(entry)]
#            else:
#                self.donorlist.append(Donor.from_json_dict(entry))

    def save_donors(self, filename='donor_list.txt'):
        with open(filename, 'w') as f:
            for donor in self.donorlist:
                f.write("{};{};{}\n".format(donor.first_name, donor.last_name,
                                            ','.join(str(a) for a in donor.donations)))

#    def save_donors(self, filename='donor_list.json'):
#        jc_donorlist = [x.to_json_compat() for x in self.donorlist]
#        with open(filename, 'w') as f:
#            json.dump(jc_donorlist, f)

    @property
    def names(self):
        return [(donor.last_name, donor.first_name) for donor in self.donorlist]

    def find(self, first, last):
        if (last, first) in self.names:
            return self.donorlist[self.names.index((last, first))]
        else:
            return None

    def update(self, first, last, amount):
        if (last, first) in self.names:
            self.find(first, last).add_donation(amount)
        else:
            self.add_donor(first, last, amount)

    def challenge(self, factor, min_donation=None, max_donation=None):
        self.save_donors()
        new_data = DonorCollection()
        new_data.load_donors()
        for donor in new_data.donorlist:
            donor.challenge(factor, min_donation, max_donation)
        return new_data
