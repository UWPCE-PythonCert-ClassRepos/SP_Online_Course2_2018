#!/usr/bin/env python

"""This module runs the mailroom script using oop paradigm."""
import sys
from datetime import date
from functools import reduce
import logging
from mailroom_model import Donor, Donation, SqliteDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self, database):
        self.database = database

    def add_donor_donation(self, name, amount):
        self.add_donor(name)
        self.add_donation(name, amount)
        self.update_stats(name)

    def add_donor(self, name):
        """Add donor."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                donor = Donor.create(
                    full_name=name
                )
                donor.save()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def add_donation(self, name, amount):
        """Add donation."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                donation = Donation.create(
                    amount=amount,
                    donor_name=name
                )
                donation.save()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def update_stats(self, name):
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            total = 0
            num = 0

            for donation in Donation.select().where(
                    Donation.donor_name == name):
                total += donation.amount
                num += 1

            with self.database.transaction():
                donor = Donor.get(Donor.full_name == name)
                donor.avg_donation = total / num
                donor.total_donation = total
                donor.num_donations = num
                donor.save()

        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def print_donor_and_amount(self, fullname, amount):
        self.add_donor_donation(fullname, amount)
        print(self._format_letter(fullname, amount))

    def list_donors(self):
        """Return all donors name."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select():
                print(donor.full_name)
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def create_report(self):
        """Return a summary report of donations."""
        header = '\nDonor Name                | Total Given |' \
                 ' Num Gifts | Average Gift'
        print(header)
        print('-' * (len(header) - 1))

        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select().order_by(Donor.total_donation.desc()):
                print('{:<26} ${:>11,.2f} {:>11d}  ${:>12,.2f}'.format(
                    donor.full_name, donor.total_donation,
                    donor.num_donations, donor.avg_donation))
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def send_letters(self):
        """Create thank you letter for each donor and save as text files"""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select():
                name = donor.full_name
                amount = donor.total_donation
                filename = f'{name}_{date.today()}.txt'
                with open(filename, 'w') as outfile:
                    # use last donated amount
                    outfile.write(self._format_letter(name, amount))
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    @staticmethod
    def _format_letter(name, amount):
        """Return formatted letter with donor name and donated amount"""
        return ('Dear {},\n\n'
                '    Thank you for your very kind donation of ${:,.2f}.\n\n'
                '    It will be put to very good use.\n\n'
                '                   Sincerely,\n'
                '                   -The Team'.format(name, amount))


def menu_selection(prompt, selection_dict):
    """Return options for user to select from."""
    while True:
        try:
            userinput = input(prompt)
            if userinput == 'q':
                break
            else:
                selection_dict[userinput]()
        except KeyError:
            print('\n{} is not a valid selection. '
                  'Please try again!'.format(userinput))


def fullname_input():
    """Return prompt asking for full name."""
    return input('Enter a donor first and last name > ').title()


def amount_input():
    """Return prompt asking for donation amount."""
    while True:
        try:
            return float(input('Enter donation amount! > '))
        except ValueError:
            print('\nPlease enter dollar amount and NOT text!')


def send_thankyou_email():
    """Return a menu selection to send thank you email to donor."""
    menu_selection(thankyou_prompt, thankyou_dict)


# Initialize database
db = DataBase(SqliteDatabase('donation.db'))

main_prompt = ('\nEnter "q" to "Exit Menu" \n'
               'Enter "1" to "Send a Thank You" \n'
               'Enter "2" to "Create a Report" \n'
               'Enter "3" to "Send Letters to Everyone" \n'
               'What do you want to do? > '
               )

main_dict = {'1': send_thankyou_email,
             '2': db.create_report,
             '3': db.send_letters
             }

thankyou_prompt = ('\nEnter "q" to "Exit Menu" \n'
                   'Enter "1" to "List Donors" \n'
                   'Enter "2" to "Enter a Donor Name" \n'
                   'What do you want to do? > '
                   )

thankyou_dict = {'1': db.list_donors,
                 '2': lambda: db.print_donor_and_amount(fullname_input(),
                                                        amount_input())
                 }


if __name__ == "__main__":
    menu_selection(main_prompt, main_dict)
