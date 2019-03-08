"""entry point to mailroom application"""

import logging
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
                         '3': send_thank_you_letters,
                         '4': edit_donation_menu}
    user_input = ('Options:\n'
                  '\t1: Create Donation\n'
                  '\t2: Create Donor Report\n'
                  '\t3: Send donors Thank Yous\n'
                  '\t4: Edit Records\n'
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
            controller.create_donation(donor=donor_selection,
                                       amount=donation_amount)
            break


def donor_report_menu():
    """creates donor report for user"""
    controller.donor_report()


def send_thank_you_letters():
    """sends thank you letters to all our donors"""
    controller.send_letters_to_everyone()


def edit_donation_menu():
    """menu to control editing the donations.  The donation
    database allows modification of donations but not of donors.  Donation
    amounts and dates can be modified.

    To support editing donation, this menu provides ability for user to
    explore donations prior to selecting edits."""

    MENU_OPTIONS = {
                    '1': controller.display_donors,
                    '2': list_donations,
                    '3': edit_donations,
                    '4': edit_donor,
                    '5': delete_donation,
                    '6': delete_donor,
                    }
    user_input = ('Options:\n'
                  '\t1: List Donors\n'
                  '\t2: List Donations for Donor\n'
                  '\t3: Edit Donation\n'
                  '\t4: Edit Donor\n'
                  '\t5: Delete Donation\n'
                  '\t6: Delete Donor\n'
                  '\t0: Quit\n'
                  'Please input number for option: ')

    menu_selection(user_input, MENU_OPTIONS)


def list_donations():
    """displays a list of donations for the donor"""
    donor = input('Input Donor Name: ')
    controller.display_donor_donations(donor)


def edit_donations():
    donation_id = int(input('Input donation id: '))
    donation = Donation.get(Donation.id == donation_id)
    print(f'donation.id: {donation.id} '
          f'donation.donation_donor: {donation.donation_donor} '
          f'donation.donation_amount: {donation.donation_amount} '
          f'donation.donation_date: {donation.donation_date}')
    new_donation_amount = int(input('Please enter new donation amount: '))
    # in future look at adding more options on donations here
    controller.update_donation(donation, 'donation_amount', new_donation_amount)


def edit_donor():
    """editing script for donor.  Only email edits allowed"""
    donor_name = input('Input donor name to edit: ')
    donor = Donor.get(Donor.donor_name == donor_name)
    print(f'donor.donor_name: {donor.donor_name} '
          f'donor.email: {donor.email} ')
    new_email = input('Please enter new email: ')
    # in future look at adding more options on donations here
    controller.update_donor(donor=donor, value=new_email)


def delete_donation():
    """deletes donation record from database"""
    donation_id = int(input('Input donation id: '))
    controller.delete_donation(donation_id)


def delete_donor():
    """deletes donor and donations from database"""
    donor_name = input('Input donor name to edit: ')
    controller.delete_donor(donor_name)

if __name__ == '__main__':
    main_menu()
