#!/usr/bin/env python3
"""
    Donor Class module - removed from mailroom code for usability and readability
    Only being used in the challenge and projection code

"""

import datetime
import os
#from mailroom_model import *
import logging
from pprint import pprint as pp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Donor:

    def __init__(self, firstname, lastname, fullname, donations=None):
        self._firstname = firstname
        self._lastname = lastname
        self._fullname = fullname
        self._donations = donations if donations else []

    @property
    def firstname(self):
        return self._firstname

    @property
    def lastname(self):
        return self._lastname

    @property
    def fullname(self):
        return self._lastname

    @property
    def donations(self):
        return self._donations

    def donations_total_d(self):
        """returns the total donations"""
        try:
            return sum(self._donations)
        except TypeError:
            return self._donations

    def last_donation_d(self):
        return self._donations[-1]

    def add_donation_d(self, donation):
        """adds the new donation amount to donations"""
        return self.donations.append(donation)

    def donation_count_d(self):
        """returns number of donations"""
        return len(self._donations)

    def average_donation_d(self):
        try:
            return self.donations_total_d() / self.donation_count_d()
        except TypeError:
            return self._donations


class DonorFunctions:
    """ Class to hold the functions done on/with Donors"""

    def __init__(self, donors=None):
        self.donorslist = donors if donors else []

    def add_donor(self, donor):
        self.donorslist.append(donor)

    def get_all_donors(self):
        return [d.fullname for d in self.donorslist]

    def list_all_donors(self):
        return "\n".join(self.get_all_donors())

    def send_single_thank_you_df(self):
        """function for sending thank you message-gets/ adds single donation and prints thank you"""
        donor_name = get_name_input(self.get_all_donors())
        if donor_name == "quit":
            print("No donor name entered, exiting to menu")
        else:
            donor_amount = check_number_input()

            if donor_name not in self.get_all_donors():
                firstname, lastname = donor_name.split(" ")
                self.add_donor(Donor(firstname, lastname, [donor_amount]))
            else:
                for donor in self.donorslist:
                    if donor.fullname == donor_name:
                        donor.add_donation(donor_amount)
            print('\nDear {},'.format(donor_name))
            print('''\tThank you for your generous donation of ${:,.2f}\n
                Sincerely, \nThe ChickTech Donations Department\n'''.format(
                donor_amount))

    def print_report_df(self):
        """Print report to match example from assignment for donor list """
        print()
        title = ['Donor Name', '|  Total Given ', '|   Num Gifts',
                 '  | Average Gift']
        print('{:<20}{:>14}{:^14}{:>14}'.format(title[0], title[1],
                                                title[2], title[3]))
        print('-'*65)
        print()
        # # Creating list to hold donors info for printing
        for donor in self.donorslist:
            print('{:<22}{}{:>12.2f}{:>10}{:>8}{:>12.2f}'.format(donor.fullname, '$',
                                                                 donor.donations_total(), donor.donation_count(),
                                                                 '$', donor.average_donation()))
        print()

    def send_letters_everyone(self):
        """Creates a letter for everyone in the database, and writes them to file."""
        letters_count = 0
        date = datetime.datetime.now()
        new_folder = date.strftime("%Y-%m-%d_%H-%M")
        try:
            os.mkdir(new_folder)
        except OSError:
            print("\nError with directory creation.Something must have gone wrong!\n")
            return
        for donor in self.donorslist:
            # create file in date folder titled with donor name
            filename = "./{}/{}_{}.txt".format(new_folder,
                                               donor.firstname, donor.lastname)
            with open(filename, 'w') as donor_thanks:
                letter_output = print_thank_you_total(donor)
                donor_thanks.write(letter_output)
            letters_count += 1
        print("Created {} Thank You letters in this folder: {}".format(
            letters_count, new_folder))

    def print_letters_to_everyone(self):
        '''test print all function'''
        print()
        for donor in self.donorslist:
            print(mailroom_pw.print_thank_you_total(donor))

    def print_donors(self):
        print(self.print_report_df())

    def print_donors_names(self):
        """ prints list of donors"""
        print("\nDonors")
        print("-"*20)
        print(self.list_all_donors())

    def print_donors_and_donations(self):
        """Prints all letters to screen - for view and testing"""
        print("\nDonors and donations")
        print("-"*30, "\n")
        [print(donor.fullname, "=>", donor.donations, '\n')
         for donor in self.donorslist]

    def print_donors_and_donation_totals(self):
        """Prints all letters to screen - for view and testing"""
        print("\nDonors and donations")
        print("-"*30, "\n")
        [print(donor.fullname, "=>", donor.donations_total(), '\n')
         for donor in self.donorslist]
