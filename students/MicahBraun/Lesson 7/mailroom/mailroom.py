# ---------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: mailroom.py
# DATE CREATED: 11/18/2018
# UPDATED: 11/26/2018
# PURPOSE: Lesson 07 pt.2
# DESCRIPTION:  This file contains all of the methods needed to work with the database that
#               was created in donor_class.py.  Through this class and its methods the user
#               can interact with the data in the database (view, add, delete) and print
#               data to file.
# ---------------------------------------------------------------------------------------------
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
        """
            Landing method: checks entries for existing Donor.donor_name
        """
        existing_donors = []
        for donor in Donor.select():
            existing_donors.append(donor.donor_name)
        try:
            if name in existing_donors:
                print('{} is already a donor. {:,.2f} added to'
                      ' their existing donations.'.format(name, amount))
                self.add_donation(name, amount)
                self.update_donor_stats(name)
            else:
                print('{} is a new donor. Adding {:,.2f} '
                      'as their first donation.'.format(name, amount))
                self.add_donor(name)
                self.add_donation(name, amount)
                self.update_donor_stats(name)

        except Exception as e:
            print('Error: ', e)

    def add_donor(self, name):
        """
            Method for adding donor to database
        """
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                new_donor = Donor.create(
                    donor_name=name
                )
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def add_donation(self, name, amount):
        """
            Method to add donation amount to donor
        """
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                donation = Donation.create(
                    donor_name=name,
                    donation_amount=amount
                )
                donation.save()
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def update_donor_stats(self, name):
        """
            Method to update donor's peripheral records
        """
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

    def delete_donor(self):
        """
            Removes indicated donor records (ForeignKeyField(on_delete='CASCADE')
        """
        self.list_donors()
        name = delete_name()
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
        self.list_donors()

    def add_donor_to_db(self, name, amount):
        """
            Calls landing method for entries: add_donor_donation
        """
        self.add_donor_donation(name, amount)

    def list_donors(self):
        """
            Return all donors' names
        """
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select():
                print(donor.donor_name)
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

    def create_report(self):
        """
            Return donor report of donations/stats
        """
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

    def write_letters(self):
        """
            Creates/writes thank you letters for each
             donor and saves as text files to disk
        """
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            directory = input(input_directory)
            logger.info('Preparing to write file(s) to disk...')
            for donor in Donor.select():
                name = donor.donor_name
                amount = donor.sum_all_donations
                filename = (name.replace(' ', '_') + '.txt')
                directory += filename
                with open(filename, 'w') as outfile:
                    outfile.write(self._format_letter(name, amount))
                    logger.info('Writing {} to disk...'.format(filename))
            logger.info('Done!')
        except Exception as e:
            logger.info('Error writing to disk. See error: '.format(e))
        finally:
            self.database.close()

    @staticmethod
    def make_destination(self, need_dir='y', directory=""):
        if need_dir == "y":
            directory = input(input_directory)
        destination = os.path.join(directory)
        return destination

    @staticmethod
    def _format_letter(name, amount):
        """
            Return formatted letter with donor name and donation amount
        """
        return ('''
Dear {},

Thank you for your continued support through your most recent contribution of ${:,.2f}. 
Your donation(s) over this year have been instrumental in moving towards our
fundraising goal of $100,000.00 to benefit local charities. On behalf of all
the members of the Foundation, we thank you for your generosity and look forward
to working with you in the future to build a better world!

Best wishes,

Foundation Board of Directors'''.format(name, amount))


def enter_name():
    """
        Return prompt asking for donor name to add/check against db
    """
    return input('\nEnter donor\'s name:  ')


def delete_name():
    """
        Return prompt asking for donor's name to delete
    """
    return input('\nEnter the donor\'s name you wish to delete:  ')


def amount_input():
    """
        Return prompt asking for donation amount
    """
    while True:
        try:
            return float(input('Donation amount:  '))
        except ValueError:
            print('\nEnter numeric amounts only.')


def add_a_new_donor():
    """
        Returns a menu selection for user: add_new_donor
    """
    try:
        menu(ad_new_prompt, add_new_don)
    except IntegrityError:
        print('Ooops! is already a donor!')
    except Exception as e:
        print(e)


def menu(prompt, selection_dict):
    """
        Returns menu selection for user: main_menu
    """
    while True:
        try:
            userinput = input(prompt).upper()
            selection_dict[userinput]()
        except ValueError:
            print('Choose A, B, C, D or Q')


def back_to_main():
    """
        Function allows user to move back to main menu
    """
    menu(prompt=user_choice, selection_dict=selection)


db = DataBase(SqliteDatabase('mailroom.db'))


selection = {
    'A': add_a_new_donor,
    'B': db.delete_donor,
    'C': db.create_report,
    'D': db.write_letters,
    'Q': sys.exit
}

user_choice = '''

--------------------------------------------------------------------------------------------------------------
                                                MAIL ROOM MENU
--------------------------------------------------------------------------------------------------------------

                                             -- Menu Options --

                                        A. Add a new Donor
                                        B. Delete Donor from database
                                        C. Display Donor Report
                                        D. Print Thank-You letters to file
                                        Q. Quit

                                        Menu Selection:  '''
ad_new_prompt = '''

--------------------------------------------------------------------------------------------------------------
                                              ADD NEW DONOR
--------------------------------------------------------------------------------------------------------------
                                    
                                        A. List Current Donors
                                        B. Enter a Donor\'s name
                                        Q. -- Go back --
                                        
                                        Make a selection:  '''

input_directory = '\nChoose file-path or press enter for default:  '


add_new_don = {'A': db.list_donors, 
               'B': lambda: db.add_donor_to_db(enter_name(), amount_input()), 
               'Q': back_to_main}


if __name__ == '__main__':
    menu(user_choice, selection)
