#!/usr/bin/env python

"""This module runs the mailroom script using oop paradigm."""
import sys
from datetime import date
from functools import reduce
import logging
from mailroom_model import Donor, Donation, SqliteDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# database = SqliteDatabase('personjob.db')


# class D:
#     def __init__(self, firstname, lastname, donations=None):
#         pass


#     def factordonation(self, factor, min_donation, max_donation):
#         return list(map(
#             lambda x: x * factor,
#             self.filter_donations(self.donations, min_donation, max_donation)))

#     @staticmethod
#     def filter_donations(donations, min_donation, max_donation):
#         if max_donation is None:
#             return list(filter(lambda x: x >= min_donation, donations))
#         else:
#             return list(filter(lambda x: min_donation <= x <= max_donation,
#                                donations))


class DataBase:

    def __init__(self, database):
        self.database = database

    def add_donation(self, name, amount):
        """Add donation."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select():
                with self.database.transaction():
                    if name == donor.name:  # append to existing donor
                        logging.info(f'{name} existed')
                        donation = Donation.create(
                            amount=amount,
                            donor=name
                        )
                        donation.save()
                        self.update_donor_stats(name, amount)
                    else:  # creata new donor
                        donor = Donor.create(
                            name=name,
                            avg_donation=amount,
                            total_donation=amount,
                            num_donations=1
                        )
                        donor.save()

                        donation = Donation.create(
                            amount=amount,
                            donor=name
                        )
                        donation.save()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def update_donor_stats(self, name, amount):
        """Update donor to date donations stats."""
        try:
            donor = Donor.get(Donor.name == name)
            donor.total_donation += amount
            donor.num_donations += 1
            donor.avg_donation = donor.total_donation / donor.num_donations
            donor.save()

        except Exception as e:
            logger.info(e)

    def print_donor_and_amount(self, fullname, amount):
        self.add_donation(fullname, amount)
        print(self._format_letter(fullname, amount))

    def list_donors(self):
        """Return all donors name."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select():
                print(donor.name)
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
            for donor in Donor.select().order_by(Donor.total_donation):
                print('{:<26} ${:>11,.2f} {:>11d}  ${:>12,.2f}'.format(
                    donor.name, donor.total_donation,
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
                name = donor.name
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

    def challenge(self, factor, min_donation=0, max_donation=None):
        # db2 = DataBase()
        # for donor in self.donors:
        #     db2.add_donor_and_amount(
        #         donor.fullname,
        #         donor.factordonation(factor, min_donation, max_donation))
        # db2.create_report()
        # return db2
        pass

    def projection(self, projection_inputs):
        # factor, min_donation, max_donation = projection_inputs
        # db2 = self.challenge(factor, min_donation, max_donation)
        # total = reduce(lambda x, y: x + y,
        #                map(lambda x: x.totaldonation, db2.donors))
        # print(f'\nProjection: total contribution would be ${total:.2f}!')
        pass


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


def factor_input():
    """Return prompt asking for challenge factor."""
    while True:
        try:
            return float(input('Enter challenge factor! > '))
        except ValueError:
            print('\nPlease enter challenge factor and NOT text!')


def projection_input():
    """Return prompt asking for challenge factor, min, and max donation to run
    projections."""
    while True:
        string = input(
            '\nEnter challenge factor, min, and max donation! \n'
            'Challenge factor, min, and max donations are optional \n'
            'Ex1: ",," will return a factor of 1 for all contributions \n'
            'Ex2: "2,,100" will double all contributions under $100 \n'
            'Ex3: "3,50," will triple all contributions above $50 > ')
        inputs = string.split(',')
        try:
            if inputs[0] == '':
                inputs[0] = 1
            if inputs[1] == '':
                inputs[1] = 0
            if inputs[2] == '':
                inputs[2] = None
            return [input if input is None
                    else float(input)
                    for input in inputs]
        except IndexError:
            print('Provide at least 2 commas!')
        except ValueError:
            print('Enter number between commas and not texts!')


def send_thankyou_email():
    """Return a menu selection to send thank you email to donor."""
    menu_selection(thankyou_prompt, thankyou_dict)

# Initialize database
db = DataBase(SqliteDatabase('donation.db'))

main_prompt = ('\nEnter "q" to "Exit Menu" \n'
               'Enter "1" to "Send a Thank You" \n'
               'Enter "2" to "Create a Report" \n'
               'Enter "3" to "Send Letters to Everyone" \n'
               'Enter "4" to "Challenge Donations" \n'
               'Enter "5" to "Create Projections" \n'
               'What do you want to do? > '
               )

main_dict = {'1': send_thankyou_email,
             '2': db.create_report,
             '3': db.send_letters,
             '4': lambda: db.challenge(factor_input()),
             '5': lambda: db.projection(projection_input())
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
