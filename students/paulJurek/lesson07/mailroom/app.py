"""entry point to mailroom application"""

import logging
from pathlib import Path
from mailroom.DonationController import DonationController
from mailroom.helpers import menu_selection
from mailroom.Donation import Donation
from mailroom.Donor import Donor
from mailroom.config import database

from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')
database.create_tables([Donation, Donor])

# start initial controller
controller = DonationController()

def main_menu():
    """calls main menu for program"""
    MAIN_MENU_OPTIONS = {'1': create_donation_menu,
                         '2': donor_report_menu,
                         '3': send_thank_you_letters}
    user_input = ('Options:\n'
                  '\t1: Create Donation\n'
                  '\t2: Create Donor Report\n'
                  '\t3: Send donors Thank Yous\n'
                  '\t0: Quit\n'
                  'Please input number for option: ')

    menu_selection(user_input, MAIN_MENU_OPTIONS)


def create_donation_menu():
    """calls create donation menu
    
    this menu allows users to create donations for users"""

    while True:
        donor_selection = input('Please input donor: ')

        if donor_selection.lower().strip() == 'list':
            # displays existing donors
            controller.display_donors()
            continue
        elif donor_selection.lower().strip() == 'quit':
            break
        else:
            donation_amount = int(input("Select donation amount: "))
            controller.create_donation(donor=donor_selection, amount=donation_amount)
            
            break


def donor_report_menu():
    """creates donor report for user"""
    controller.donor_report()


def send_thank_you_letters():
    """sends thank you letters to all our donors"""
    controller.send_letters_to_everyone()

if __name__ == '__main__':
    main_menu()
