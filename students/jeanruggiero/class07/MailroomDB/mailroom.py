#!/usr/bin/env python

"""
This script maintains a database of donors including name and donation
amounts
"""

import datetime
import donor_report
from mailroom_model import *
from peewee import *


# Define exception to exit script
class ExitScript(Exception):
    pass


# Define main menu functions
def add_donation():
    """Add a donation to donors dict and compose a thank you email."""

    with database.transaction():
        while True:
            name = input("Enter the donor's Full Name, or 'list': ").lower()
            if name == 'return':
                return
            elif name == 'list':
                for donor in (Donor.select()):
                    print(donor.name)
            else:
                try:
                    new_donor = Donor.create(
                        name=name,
                        date_added=datetime.date.today()
                        )
                    new_donor.save()
                    break
                except IntegrityError:
                    print('This donor already exists. Adding a new donation...')
                    break

        while True:
            amount = input('Enter the donation amount: ')
            if amount.lower() == 'return':
                return
            try:
                amount = float(amount)
                new_donation = Donation.create(
                    amount=amount,
                    date=datetime.date.today(),
                    donor=name
                    )
                new_donation.save()
                break
            except ValueError:
                print('Please enter a number value for donation amount.')

        print(); print(thank(name, amount))


def create_report():
    """Print a report of donors with a summary of their donation history."""
    donor_report.create_report()


def send_letters():
    """
    Create thank you letters to all donors thanking them
    for their most recent donation.
    """

    d = datetime.date.today()
    thanked_donors = []
    for donor in Donor.select():
        donations = (Donation
                     .select()
                     .where(Donation.donor == donor)
                     .order_by(-Donation.date))

        if donor not in thanked_donors:
            filename = '_'.join([donor.name.replace(' ', '_'), str(d.month),
                                 str(d.day), str(d.year)]) + '.txt'
            with open(filename, 'w') as f:
                f.write(thank(donor.name, donations[0].amount))

            thanked_donors.append(donor)


def delete_donor():
    """
    Delete a donor from the database.
    """
    with database.transaction():
        while True:
            name = input("Enter the donor's Full Name, or 'list': ").lower()
            if name == 'return':
                return
            elif name == 'list':
                for donor in (Donor.select()):
                    print(donor.name)
            else:
                donor_del = Donor.get(Donor.name == name)
                donor_del.delete_instance(recursive=True)
                break
    pass


def quit():
    database.close()
    raise ExitScript


# Define helper functions
def thank(name, amount):
    """Return a string thanking donor name for a donation of amount."""
    donor = Donor.get(Donor.name == name)
    return f"Dear {name},\n\n" + \
        "Thank you so much for your generous donation of " + \
        f"${amount:.2f}.\n\nWe really appreciate your donations " + \
        f"totalling ${donor.donation_total:.2f}.\n" + \
        "Sincerely, The Wookie Foundation"


if __name__ == '__main__':

    database = SqliteDatabase('mailroom.db', pragmas={'foreign_keys': 1})
    database.connect()

    actions = {
               '1': add_donation,
               '2': create_report,
               '3': send_letters,
               '4': delete_donor,
               '5': quit
               }

    # User interaction
    while True:
        try:
            # Main menu - prompt user for an action
            print('''
                \nSelect an action to perform...\n
                Type "return" at any time to return to main menu.
                ''')
            action = input('''
                1: Add a Donation & Send Thank You
                2: Create a Report
                3: Send Letters to Everyone
                4: Delete a Donor
                5: Quit\n
                ''')
            actions.get(action)()
        except ExitScript:
            break
        # except TypeError:
        #     if action not in actions:
        #         continue
