#!/usr/bin/env python

"""
This script maintains a database of donors including name and donation
amounts
"""

import datetime
from mailroom_model import *
from peewee import *


class ExitScript(Exception):
    """Allows script exit."""
    pass


class MainMenu(Exception):
    """Allows return to main menu."""
    pass


# Define main menu functions
class Mailroom():

    def __init__(self, database_name):
        database.init(database_name, pragmas={'foreign_keys': 1})
        database.connect()

    def add_or_get_donor_add_donation(self):
        """
        Add a donation to donors dict (if not already present)
        and compose a thank you email.
        """
        try:
            with database.transaction():
                name = self.input_donor_name()
                self.add_donor(name)

                amount = self.input_donation_amount()
                self.add_donation(name, amount)

        except MainMenu:
                return

        print(self.thank(name, amount))

    def create_report(self):
        """Print a report of donors with a summary of their donation history."""
        donors = (Donor
                  .select(Donor, fn.SUM(Donation.amount).alias('total_donations'))
                  .join(Donation)
                  .group_by(Donor.name)
                  .order_by(fn.SUM(Donation.amount).desc()))


        # Determine table size_report
        table_size = self.size_report(donors)

        # Build format strings for header and table rows
        head_string = '{:{}s} | {:^{}s} | {:^{}s} | {:^{}s}'
        row_string = '{:{}s} | $ {:>{}.2f} | {:>{}d} | $ {:>{}.2f}'

        # Table header - Add 2 to width of dollar value fields to account for
        # dollar sign and space
        report_str = head_string.format(
            'Donor Name', table_size[0], 'Total Given',
            table_size[1] + 2, 'Num Gifts', table_size[2],
            'Average Gift', table_size[3] + 2) + '\n'

        # Table rows
        report_list = []
        for donor in donors:
            report_list.append(row_string.format(
                donor.name, table_size[0], donor.donation_total,
                table_size[1], donor.donation_count, table_size[2],
                donor.donation_average, table_size[3]))
        print(report_str + '\n'.join(report_list))

    def send_letters(self):
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
                    f.write(self.thank(donor.name, donations[0].amount))

                thanked_donors.append(donor)

    def delete_donor(self):
        """
        Delete a donor and their donations from the database.
        """
        try:
            name = self.input_donor_name()
            self.delete_from_db(name)
        except MainMenu:
            return

    @staticmethod
    def quit():
        database.close()
        raise ExitScript

    # Define helper functions
    def input_donor_name(self):
        """
        Get donor name input from user, support 'return' and 'list'
        functionality.
        :return: user input, or None
        """
        while True:
            name = input("Enter the donor's Full Name, or 'list': ")
            if name.lower() == 'return':
                raise MainMenu
            elif name.lower() == 'list':
                self.list_donors()
            else:
                return name

    @staticmethod
    def input_donation_amount():
        """
        Get donation amount input from the user, support 'return'
        functionality. Handle errors where input is not a number.
        :return: donation amount (float), or None
        """

        while True:
            amount = input('Enter the donation amount: ')
            if amount == 'return':
                raise MainMenu
            try:
                amount = float(amount)
                return amount
            except ValueError:
                print('Please enter a number value for donation amount.')

    @staticmethod
    def list_donors():
        """List donors from the donors database in alphabetical order."""
        for donor in (Donor.select().order_by(Donor.name)):
            print(donor.name)

    @staticmethod
    def add_donor(name):
        """
        Adds a donor with the given name to the donors database.
        :param name: donor's full name
        :return: None
        """
        try:
            new_donor = Donor.create(
                name=name,
                date_added=datetime.date.today()
                )
            new_donor.save()
            print('Donor not in database. Adding donor.')
        except IntegrityError:
            print('This donor already exists. Adding a new donation...')

    @staticmethod
    def add_donation(name, amount):
        """
        Adds a donation to the donors database.
        :param name: donor's full name
        :param amount: donation amount
        :return: None
        """
        new_donation = Donation.create(
            amount=amount,
            date=datetime.date.today(),
            donor=name
            )
        new_donation.save()

    @staticmethod
    def size_report(donors):
        """Determine column widths for a donor report."""
        # Determine width of columns based on data in donors data structure
        # Convert numbers to strings to determine their length in characters
        # Convert the dollar amounts to an integer to remove decimal places (since
        # there are an unknown number of them), then add 3 to the length to
        # accommodate for a period and 2 decimal places
        # Ensure column size is at least as wide as header text

        name_width = max(len(donor.name) for donor in donors)
        name_width = max(name_width, len('Donor Name'))

        total_width = max(len(str(int(
            donor.donation_total))) for donor in donors) + 3
        total_width = max(total_width, len('Total Given'))

        num_width = max(len(str(donor.donation_count)) for donor in donors)
        num_width = max(num_width, len('Num Gifts'))

        avg_width = max(len(str(int(
            donor.donation_average))) for donor in donors) + 3
        avg_width = max(avg_width, len('Average Gift'))

        return [name_width, total_width, num_width, avg_width]

    @staticmethod
    def delete_from_db(name):
        """
        Deletes a donor and their donations from the database.
        :param name: donor's full name
        :return: None
        """

        try:
            donor_del = Donor.get(Donor.name == name)
            donor_del.delete_instance(recursive=True)
        except DoesNotExist:
            print("This donor doesn't exist.")

    @staticmethod
    def thank(name, amount):
        """Return a string thanking donor name for a donation of amount."""
        donor = Donor.get(Donor.name == name)
        return f"Dear {name},\n\n" + \
            "Thank you so much for your generous donation of " + \
            f"${amount:.2f}.\n\nWe really appreciate your donations " + \
            f"totalling ${donor.donation_total:.2f}.\n" + \
            "Sincerely, The Wookie Foundation"

    def main_menu(self):
        """
        Contains the UI for the mailroom script.
        :return: None
        """
        actions = {
            '1': self.add_or_get_donor_add_donation,
            '2': self.create_report,
            '3': self.send_letters,
            '4': self.delete_donor,
            '5': self.quit
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
            except TypeError as t:
                if action not in actions:
                    continue
                else:
                    raise t


if __name__ == '__main__':

    mailroom = Mailroom('mailroom.db')
    mailroom.main_menu()

