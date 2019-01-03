"""
    Assignment 2: Run Mailroom
    Converting my mailroom code in Cindy's format....
"""

import logging
from create_db import *
from populate_db import *
from mailroom import *
from peewee import *

from datetime import date
import sys


# collection = Donation() # Cindy creates instance... I didn't...

options = {1: 'Add or Update Donor', 2: 'Create a Report', 3: 'Delete a Donor', 4: 'Quit'}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('mailroom.db')
logger.info('mailroom database input and output operations')


def add_donor(): # in mailroom.py
    #full_name = 'Enter a full name: '
    #donation_amount = 'Enter donation amount: '
    #response = input(full_name)

    donor_name = str(input("Full Name: "))
    return donor_name

    """
    while donor_name == 'list':
        print("\n".join(collection.donors))
        response = input(full_name)
        while response.upper() != 'Q':
            amount_input = input(donation_amount)
            if amount_input.upper() != 'Q':
                try:
                    amount = float(amount_input)
                    donor = Donor(response, [amount])
                    collection.add_update(donor)
                    print(donor.get_letter_text(response, amount))
                except ValueError:
                    print('Input must be a float. try again')
    """

def add_donation(): # in mailroom.py
    pass


def make_donation(): # in mailroom.py
    pass


def create_report(): # in mailroom.py
    print(collection.generate_report())


def delete_donor(): # NOT in mailroom.py
    command_prompt = 'Enter a donor name to delete: '
    aName = input(command_prompt)
    collection.delete(aName)


def select_quit(): # in mailroom.py
    pass


def quit(): # in mailroom.py
    return 'exit menu'


def select_mainmenu(): # in mailroom.py
    print('\nChoose an action: ')
    options = ['1. Add or update Donor', '2. Create a Report', '3. Delete a Donor', '4. Quit']
    option_str = '\n'.join(['\t'+item for item in options])
    print(option_str)


def select_submenu(): # in mailroom.py
    pass


def print_list(): # in mailroom.py
    pass


def thank_you_loop(): # in mailroom.py
    pass



def send_letters(): # in mailroom.py
    pass


def main():
    choice = ''
    selection = 'Select an option (1,2,3, or 4) ===>'
    switch_function_dict = {'1': add_update_donor, '2': create_report, '3': delete_donor, '4': quit}

    database.connect()
    database.execute_Sql('PRAGMA foreign_keys = ON;')

    for db_donor in Donor_Collection:
        amounts = []
        amount_list = Donation_Amount.select().where(Donation_Amount.from_person == db_donor.person_name)
        for amount in amount_list:
            amounts.append(amount.donation_amount)
        donor = Donor(db_donor.person_name, amounts)
        collection.insert_donor(donor)

    database.close()
    while True:
        display_main_menu()
        choice = input(selection)
        try:
            if switch_function_dict[choice]() == 'exit menu':
                break
        except KeyError:
            print("Please enter 1,2,3, or 4")


if __name__ == '__main__':
    main()


