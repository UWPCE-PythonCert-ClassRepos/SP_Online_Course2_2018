# ------------------------------------------------- #
# Title: Lesson 7, Database Management, Mail Room
# Dev:   Craig Morton
# Date:  12/20/2018
# Change Log: CraigM, 1/2/2019, Database Management, Mail Room
# ------------------------------------------------- #

# Mail room interface

import sys
import logging
from peewee import *
from donor_class import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self, database):
        self.database = database

    def add_donor_donation(self, name, amount):
        """Check for Donor entries."""
        existing_donors = []
        for donor in Donor.select():
            existing_donors.append(donor.donor_name)
        try:
            if name in existing_donors:
                print('{} is already a donor. {:,.2f} added to'
                      ' their donations.'.format(name, amount))
                self.donation_add(name, amount)
                self.update_donor_status(name)
            else:
                print('{} is a new Donor. Adding {:,.2f} '
                      'for their initial donation.'.format(name, amount))
                self.donor_add(name)
                self.donation_add(name, amount)
                self.update_donor_status(name)
        except Exception as e:
            print('Error! ', e)

    def donor_add(self, name):
        """Adds Donor to database."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                new_donor = Donor.create(
                    donor_name=name)
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def donation_add(self, name, amount):
        """Add donation to Donor."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                donation = Donation.create(
                    donor_name=name,
                    donation_amount=amount)
                donation.save()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def update_donor_status(self, name):
        """Update Donor records."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            sum_gifts = 0
            num_gifts = 0
            for donation in Donation.select().where(
                    Donation.donor_name == name):
                sum_gifts += donation.donation_amount
                num_gifts += 1
            with self.database.transaction():
                donor = Donor.get(Donor.donor_name == name)
                donor.sum_all_donations = sum_gifts
                donor.count_all_donations = num_gifts
                donor.avg_all_donations = sum_gifts / num_gifts
                donor.save()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def donor_delete(self):
        """Delete Donor records."""
        self.donors_list()
        name = name_deletion()
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                donor = Donor.get(Donor.donor_name == name)
                donor.delete_instance()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()
        self.donors_list()

    def db_add_donor(self, name, amount):
        """Write Donor donation to database."""
        self.add_donor_donation(name, amount)

    def donors_list(self):
        """List Donors."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select():
                print(donor.donor_name)
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def report_create(self):
        """Generate Donor report."""
        header = '\nDonor Name                |  Total Given  |' \
                 ' Num Gifts | Average Gift'
        print(header)
        print('-' * (len(header) - 1))
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select().order_by(Donor.sum_all_donations.desc()):
                print('{:<26}  ${:>11,.2f} {:>11d}   ${:>12,.2f}'.format(
                    donor.donor_name, donor.sum_all_donations,
                    donor.count_all_donations, donor.avg_all_donations))
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def letter_creation(self):
        """Writes thank you letters for all Donors to disk."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            directory = input(input_directory)
            logger.info('Sending letters to directory')
            for donor in Donor.select():
                name = donor.donor_name
                amount = donor.sum_all_donations
                filename = (name.replace(' ', '_') + '.txt')
                directory += filename
                with open(filename, 'w') as outfile:
                    outfile.write(self.letter_format(name, amount))
                    logger.info('Writing {} to disk'.format(filename))
            logger.info('Letters sent!')
        except Exception as e:
            logger.info('Unable to write to disk!  See error: '.format(e))
        finally:
            self.database.close()

    def update_donor_name(self):
        """Changes Donor name"""
        self.donors_list()
        curr_name, new_name = name_update_input()
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                Donor.update(donor_name=new_name).where(
                    Donor.donor_name == curr_name).execute()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()
            self.donors_list()

    @staticmethod
    def destination_creation(self, need_dir='y', directory=""):
        if need_dir == "y":
            directory = input(input_directory)
        destination = os.path.join(directory)
        return destination

    @staticmethod
    def letter_format(name, amount):
        """Write Donor letter including name and donation amount."""
        return ("""Dear {}, 
Thank you for your support and contribution of ${:,.2f}. 
Your donation(s) are greatly appreciated and will be put to good use!

Highest regards,
The Charity""".format(name, amount))


def name_entry():
    """Return prompt asking for donor name to add/check against db"""
    return input('Enter a donor first and last name: ').title()


def name_update_input():
    """Return prompt asking for currenty name and new name."""
    curr_name = name_entry()
    new_name = input('Enter a new first and last name: ').title()
    return curr_name, new_name


def name_deletion():
    """Return prompt asking for donor's name to delete"""
    return input('\nPlease enter the full name of the Donor you wish to delete:  ').title()


def input_amount():
    """Return prompt asking for donation amount"""
    while True:
        try:
            return float(input('Please enter the donation amount:  '))
        except ValueError:
            print('\nPlease only enter numeric values.')


def add_new_donor():
    """Returns a menu selection for user: add_new_donor"""
    try:
        menu(add_new_menu, add_new_don)
    except IntegrityError:
        print('Error!  Donor already exists.')
    except Exception as e:
        print(e)


def menu(prompt, selection_dict):
    """Returns menu selection for user: main_menu"""
    while True:
        try:
            userinput = input(prompt).title()
            selection_dict[userinput]()
        except ValueError:
            print('Choose A, B, C, D or E')


def main_return():
    """Function allows user to move back to main menu"""
    menu(prompt=main_menu, selection_dict=user_choice)


db = DataBase(SqliteDatabase('mailroom.db'))

user_choice = {
    'A': add_new_donor,
    'B': db.update_donor_name,
    'C': db.donor_delete,
    'D': db.report_create,
    'E': db.letter_creation,
    'F': sys.exit}

main_menu = """

                                            MAIN MENU

                                        A> Add new Donor
                                        B> Update Donor name
                                        C> Delete Donor
                                        D> Generate Donor report
                                        E> Send Donor letters
                                        F> Exit
                                        Please select an option:  """
add_new_menu = """

                                            ADD DONOR

                                        A> List of Donors
                                        B> Enter Donor name
                                        E> Return to Main Menu

                                        Please select an option:  """

input_directory = '\nPress Enter to write to the local directory or specify a file path:  '

add_new_don = {'A': db.donors_list,
               'B': lambda: db.db_add_donor(name_entry(), input_amount()),
               'E': main_return}

if __name__ == '__main__':
    menu(main_menu, user_choice)
