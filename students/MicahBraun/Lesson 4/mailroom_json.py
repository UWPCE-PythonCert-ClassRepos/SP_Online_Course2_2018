# --------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: mailroom_json.py
# DATE CREATED: 11/4/2018
# UPDATED: 11/7/2018
# PURPOSE: Lesson 04
# DESCRIPTION: Class data for individual donor fields and donor dictionary func-
# -tions.
# --------------------------------------------------------------------------------
from json_save_dec import json_save
from saveables import String, List


@json_save
class EachDonor:
    """
    Individual donor field behaviors
    """
    name = String()
    each_donation = List()

    def __init__(self, name, each_donation):
        """
        Initialize instance objects
        :param name: name object for individual donors
        :param each_donation: individual donations (to be added to list)
        """
        self.name = name
        self.each_donation = []
        for new_donation in each_donation:
            self.each_donation.append(new_donation)

    def new_donation(self, amnt):
        """
        Donation adder() function -- allows user to enter
        new donation amount(s) for a specific donor.
        :param amnt: donation amount (numeric)
        :return: N/A
        """
        self.each_donation.append(amnt)

    def write_letter(self, *args):
        """
        Pre-written text with donor info to be added on
        individual run
        :param args:
        :return:
        """
        donor_container = {'name': self.name, 'donation': self.each_donation[-1],
                           'num_donations': len(self.each_donation)}
        thankyou_file = ('''
Dear {name},

Thank you for your continued support through your most recent contribution of ${donation:,.2f}. 
Your {num_donations} donation(s) over this year have been instrumental in moving towards our
fundraising goal of $100,000.00 to benefit local charities. On behalf of all
the members of the Foundation, we thank you for your generosity and look forward
to working with you in the future to build a better world!

Best wishes,

Foundation Board of Directors\n'''.format(**donor_container))

        return thankyou_file

    @property
    def sum_donations(self):
        """
        Returns sum of donor's donations
        :return:
        """
        return sum(self.each_donation)

    @property
    def num_donations(self):
        """
        Returns number of donations for self.donor
        :return:
        """
        return len(self.each_donation)

    @property
    def avg_donations(self):
        """
        Returns average value of donations for self.donor
        :return:
        """
        return sum(self.each_donation) / len(self.each_donation)

    def __str__(self):
        """
        Formatting for report columns
        :return:
        """
        return "{:<20}{:>15,.2f}{:^18}{:>10,.2f}".\
            format(self.name, self.sum_donations, self.num_donations, self.avg_donations)

    def __repr__(self):
        """
        :return:
        """
        return "Donor(\'{}\', {})".format(self.name, self.each_donation)

    def __lt__(self, other):
        return self.sum_donations < other.sum_donations

    def __gt__(self, other):
        return self.sum_donations > other.sum_donations

    def __eq__(self, other):
        return self.sum_donations == other.sum_donations

    def __ne__(self, other):
        return self.sum_donations != other.sum_donations


@json_save
class DonorList:

    donor_dict = List()

    def __init__(self, *args):
        self.donor_dict = []
        for addition in args:
            self.donor_dict.append(addition)

    def add_(self, *args):
        for donor in args:
            self.donor_dict.append(donor)

    def check_(self, chk_name):
        found_flag = False
        for donor in self.donor_dict:
            if chk_name == donor.name:
                found_flag = True
        return found_flag

    def get_(self, name):
        for donor in self.donor_dict:
            if name == donor.name:
                return donor

    def sort_list(self):
        return sorted(self.donor_dict, reverse=True)

    def report(self):
        print()
        print("Donor Name           |  Total Given  | Num Gifts |  Average Gift")
        for donor in self.sort_list():
            print(donor)

    def save_(self, fname, info):
        name = "{}.json".format(fname)
        with open(name, 'w') as f:
            f.write(info)

    def __iter__(self):
        return self

    def __str__(self):
        return "\n".join(donor.name for donor in self.donor_dict)
