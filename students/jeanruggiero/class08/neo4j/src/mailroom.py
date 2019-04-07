#!/usr/bin/env python

"""
This script maintains a database of donors including name and donation
amounts
"""

import datetime
import statistics
import login_database
from pprint import pprint


class ExitScript(Exception):
    """Allows script exit."""
    pass


class MainMenu(Exception):
    """Allows return to main menu."""
    pass


# Define main menu functions
class Mailroom():

    def add_or_get_donor_add_donation(self):
        """
        Add a donation to donors dict (if not already present)
        and compose a thank you email.
        """
        try:
            name = self.input_donor_name()
            amount = self.input_donation_amount()

            self.add_donor(name)
            self.add_donation(name, amount)

        except MainMenu:
            return

        print(self.thank(name, amount))

    def create_report(self):
        """Print a report of donors with a summary of their donation history."""
        donors = self.get_donors()

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
        for donor in sorted(donors.keys(), key=lambda x: sum(donors[x]), reverse=True):
            report_list.append(row_string.format(
                donor, table_size[0], sum(donors[donor]),
                table_size[1], len(donors[donor]), table_size[2],
                statistics.mean(donors[donor]), table_size[3]))
        print(report_str + '\n'.join(report_list))

    def send_letters(self):
        """
        Create thank you letters to all donors thanking them
        for their most recent donation.
        """
        d = datetime.date.today()
        thanked_donors = []
        donors = self.get_donors()
        for donor in donors:
            if donor not in thanked_donors:
                filename = '_'.join([donor.replace(' ', '_'), str(d.month),
                                     str(d.day), str(d.year)]) + '.txt'
                with open(filename, 'w') as f:
                    f.write(self.thank(donor, donors[donor][0]))

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

    def list_donors(self):
        """List donors from the donors database in alphabetical order."""
        for donor in sorted(self.get_donors().keys()):
            print(donor)

    def add_donor(self, name):
        """
        Adds a donor with the given name to the donors database.
        :param name: donor's full name
        :return: None
        """
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph = """
                MATCH (d:Donor {name: '%s'})
                RETURN d.name as name
                """ % name
            if session.run(cyph).value():
                print('This donor already exists. Adding a new donation...')
                return
            else:
                print('Donor not in database. Adding donor.')
                cyph = "CREATE (n:Donor {name:'%s', date_added:'%s'})" % (
                    name, datetime.date.today().isoformat())
                session.run(cyph)

    def add_donation(self, name, amount):
        """
        Adds a donation to the donors database.
        :param name: donor's full name
        :param amount: donation amount
        :return: None
        """
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph = "CREATE (n:Donation {amount:%.2f, date:'%s'})" % (
                amount, datetime.date.today().isoformat())
            session.run(cyph)
            cyph = """
                MATCH (d1:Donor {name:'%s'})
                CREATE (d1)-[donated:DONATED]->(a1:Donation {amount: %.2f, date: '%s'})
                RETURN d1
                """ % (name, amount, datetime.date.today().isoformat())
            session.run(cyph)

    def get_donors(self):
        """Returns a dictionary of all donors and their donations."""
        donor_dict = {}

        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph = """
                MATCH (d:Donor)
                RETURN d.name as name
                """
            donors = session.run(cyph)

            for donor in donors:
                cyph = """
                    MATCH (d1 {name:'%s'})
                        -[:DONATED]->(donations)
                    RETURN donations""" % donor['name']
                donations = session.run(cyph)
                donation_list = []
                for rec in donations:
                    for donation in rec.values():
                        donation_list.append((donation['amount'], donation['date']))
                donor_dict[donor['name']] = [donation[0] for donation in
                                             sorted(donation_list, key=lambda x:x[1], reverse=True)]

        return donor_dict

    @staticmethod
    def size_report(donors):
        """Determine column widths for a donor report."""
        # Determine width of columns based on data in donors data structure
        # Convert numbers to strings to determine their length in characters
        # Convert the dollar amounts to an integer to remove decimal places (since
        # there are an unknown number of them), then add 3 to the length to
        # accommodate for a period and 2 decimal places
        # Ensure column size is at least as wide as header text

        name_width = max(len(donor) for donor in donors)
        name_width = max(name_width, len('Donor Name'))

        total_width = max(len(str(int(
            sum(donations)))) for donations in donors.values()) + 3
        total_width = max(total_width, len('Total Given'))

        num_width = max(len(str(
            len(donations))) for donations in donors.values())
        num_width = max(num_width, len('Num Gifts'))

        avg_width = max(len(str(int(
            statistics.mean(donations)))) for donations in donors.values()) + 3
        avg_width = max(avg_width, len('Average Gift'))

        return [name_width, total_width, num_width, avg_width]

    def delete_from_db(self, name):
        """
        Deletes a donor and their donations from the database.
        :param name: donor's full name
        :return: None
        """
        driver = login_database.login_neo4j_cloud()
        with driver.session() as session:
            cyph = """
                            MATCH (d:Donor {name: '%s'})
                            RETURN d.name as name
                            """ % name
            if session.run(cyph).value():
                cyph = """
                    MATCH (:Donor {name:'%s'})
                        -[r:DONATED]-(donations)
                    DELETE r""" % name
                session.run(cyph)
                cyph = """
                    MATCH (d:Donor {name:'%s'})
                    DELETE d""" % name
                session.run(cyph)
            else:
                print("This donor doesn't exist.")

    def thank(self, name, amount):
        """Return a string thanking donor name for a donation of amount."""
        donors = self.get_donors()
        total_donations = sum(donors[name])

        return f"Dear {name},\n\n" + \
            "Thank you so much for your generous donation of " + \
            f"${amount:.2f}.\n\nWe really appreciate your donations " + \
            f"totalling ${total_donations:.2f}.\n" + \
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

    mailroom = Mailroom()
    mailroom.main_menu()

