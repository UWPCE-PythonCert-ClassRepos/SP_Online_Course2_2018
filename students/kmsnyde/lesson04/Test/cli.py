# -*- coding: utf-8 -*-
"""
Created on Sun Jul  1 10:21:27 2018

@author: HP-Home
"""

from mailroom_oo import Donor, Mailroom as mr
from helpers import main_menu, set_donor_name
import sys


# Scenarios: Uncomment one before running the app

# Scenario 1: Donors data are hard coded. Can be used to save the donors

# donor1 = Donor('Ghassan', [100, 200, 300])
# donor2 = Donor('Miles', [52, 241, 736])
# donor3 = Donor('Jack', [425, 100, 245])
# donor4 = Donor('Tony', [55, 342, 765])
# mr = Mailroom([donor1, donor2, donor3, donor4])

# Scenario 2: Donors data will be loaded

# mr = Mailroom([])


def thankyou_procedure():
    donor_name = set_donor_name()
    if donor_name.lower() == 'list':
        all_donors = mr.list_donors()
        print(all_donors)
    elif donor_name in mr.all_donors():
        thx = mr.send_thankyou(donor_name)
        print(thx)
    else:
        mr.add_donor(Donor(donor_name, []))


def main():
    while True:
        users_choice = main_menu()
        selection = {
            '1': thankyou_procedure,
            '2': mr.create_report,
            '3': mr.save_report,
            '4': mr.save_donors,
            '5': mr.load_donors,
            '6': sys.exit
        }
        try:
            selection[users_choice]()
        except KeyError:
            print('Choose 1 to 6')
            pass