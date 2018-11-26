#!/usr/bin/env python3

import logging
from datetime import date
from mailroom import Donor, Donations
from create_donor import Donor_Collection, Donation_Amount
from peewee import *


collection = Donations()

options = { 1: 'Add or Update Donor', 2: 'Create a Report', 3: 'Delete a Donor', 4:'Quit'}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('donation.db')


def add_update_donor():
    """This function asks user to enter name and donation amount"""
    full_name = 'Enter a full name (enter Q to main menu): '
    donation_amount = 'Enter donation amount(enter Q to main menu):'
    response = input(full_name)
    # display all donors' names if input is 'list'
    while response == 'list':
        print("\n".join(collection.donors))
        response = input(full_name)
    # if input is not 'Q' to quit
    if response.upper() != 'Q':
        amount_input = input(donation_amount)
        if amount_input.upper() != 'Q':
            try:
                amount = float(amount_input)
                donor = Donor(response, [amount])
                collection.add_update(donor)
                # thank you email
                print(donor.get_letter_text(response, amount))
            except ValueError:
                print('Input must be a float.  try again')

def create_report():
    print(collection.generate_report())


def delete_donor():
    command_prompt = 'Enter a donor name to delete: '
    aName = input(command_prompt)
    collection.delete(aName)

def quit():
    return 'exit menu'

def display_main_menu():
    """Display main menu"""
    print('\nChoose an action:')
    options = ['1. Add or Update Donor', '2. Create a Report', '3 Delete a Donor', '4. Quit']
    option_str = '\n'.join(['\t'+item for item in options])
    print(option_str)

def main():
    choice = ''
    selection = 'Select an option (1, 2, 3, or 4) ===>'
    switch_function_dict = {'1': add_update_donor, '2': create_report, '3': delete_donor, '4': quit}

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    # update local list of donors
    for db_donor in Donor_Collection:
        amounts = []
        amount_list = Donation_Amount.select().where(Donation_Amount.from_person == db_donor.person_name)
        for amount in amount_list:
            amounts.append(amount.donation_amount)
        donor = Donor(db_donor.person_name, amounts)
        collection.insert_donor(donor)

    database.close()
    while True:
        # Display main menu
        display_main_menu()
        choice = input(selection)
        try:
            if switch_function_dict[choice]() == 'exit menu':
                break
        except KeyError:
            print("Please enter 1, 2, 3, or 4")

if __name__ == '__main__':
    main()
