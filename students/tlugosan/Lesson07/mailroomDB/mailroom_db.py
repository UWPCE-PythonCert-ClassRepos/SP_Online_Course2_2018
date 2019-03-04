#!/usr/bin/env python3
""" Automate a script to send a thank you mail, print a report of donor or quit the program."""
from operator import itemgetter
import os
import datetime
import logging
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

from mailroom_db_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DonorDB:
    def __init__(self, database):
        self.database = database

    def add_donor(self, person_name, lives_in):
        """Adds a donor only to the Donor table"""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            new_person = Donor.create(
                person_name=person_name,
                lives_in=lives_in)
            new_person.save()
            print(str(new_person.person_name) + " was succesfully added")

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def delete_donor(self, person_name):
        """Deletes a donor entireley from the database and any reference of
        it"""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                aperson = Donor.get(Donor.person_name == person_name)
                aperson.delete_instance()

            print(person_name + " was succesfully deleted")

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def add_donation(self, donor_name, donation_amount):
        """Adds a donation to the Donation table"""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                new_donation = Donations.create(
                    donor_name=donor_name,
                    donation_amount=donation_amount)
                new_donation.save()
            print("Donation was succesfully added")

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def update_donor_name(self, old_name, new_name):
        """Updated the name of a donor in all the tables"""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                update_dontation_table= (Donations
                    .update(donor_name = new_name)
                    .where(Donations.donor_name == old_name).execute())
                update_donor_table = (Donor
                    .update(person_name = new_name)
                    .where(Donor.person_name == old_name).execute())

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def calculate_report(self):
        """List of stats per each Donor: number of donations,
              total amount and average"""

        table_header = ['Donor Name', 'Total Given', 'Num Gifts',
                        'Average Gifts']
        len_header = len(table_header)
        print("|".join(["{:<20}"] * len_header).format(*table_header))
        print("-" * (20 * len_header + (len_header - 1)))
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')

            query = (Donations
                     .select(Donor.person_name, fn.COUNT(
                Donations.donation_amount).alias(
                'donation_count'), fn.SUM(Donations.donation_amount).alias(
                'total_amount'),
                             (fn.SUM(Donations.donation_amount) / fn.COUNT(
                                 Donations.donation_amount)).alias(
                                 'average'))
                     .join(Donor, JOIN.INNER)
                     .group_by(Donor)
                     .order_by(fn.SUM(Donations.donation_amount) / fn.COUNT(
                Donations.donation_amount))
                     )

            for d in query:
                print("{:<20}| ${:<19}| {:<19}| ${:<19}".format(str(
                    d.donor_name),
                    str(round(d.total_amount, 2)),
                    str(d.donation_count),
                    str(round(d.average, 2))))

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def sending_thank_you(self):

        """Lists all the donors or prompts for a name and donation amount to compile the thank you email."""
        donor_name = input("Please enter the name of the person to send "
                           "thank you note: ")
        while True:
            try:
                donation_amount = float(
                    input(
                        'What donation amount do you want to thank them for? '))
                if donation_amount > 0:
                    break
                else:
                    print("Number has to be positive.")
            except ValueError:
                print("Input must be a number.")
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            aperson = Donations.get(Donations.donor_name == donor_name and
                                    Donations.donation_amount == donation_amount)
            print(
                "Dear {}, Thank you for your generous contribution of ${:.2f} "
                "to our program.".format(aperson.donor_name,
                                         aperson.donation_amount))

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def print_db(self):
        """Prints each donnation of each donor"""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Donations
                     .select(Donor.person_name, Donations.donation_amount)
                     .join(Donor, JOIN.INNER)
                     )

            for d in query:
                print("{:<20}: ${}".format(str(d.donor_name),
                                           str(d.donation_amount)))

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def print_only_donors(self):
        """Prints a list of donors"""
        donor_list =[]
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Donor
                     .select(Donor.person_name))

            for d in query:
                donor_list.append(str(d.person_name))
                print("{}".format(str(d.person_name)))

            print(type(donor_list))

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()
            
        return donor_list

    def send_everyone_letters(self, target_directory=os.getcwd()):
        """Sends a letter to everyone in the table for their first donation in the list."""
        file_name_extension = '.txt'
        today_date_short = calculate_date()
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Donations
                     .select(Donor.person_name,
                             fn.SUM(Donations.donation_amount).alias(
                                 'total_amount'))
                     .join(Donor, JOIN.INNER)
                     .group_by(Donor)
                     )

            for file_name in query:
                target_file_path = os.path.join(target_directory,
                                                str(
                                                    file_name.donor_name).replace(
                                                    ' ',
                                                    '_') + today_date_short + file_name_extension)
                try:
                    with open(str(target_file_path), 'w') as tf:
                        letter_content = ("Dear {},\n"
                                          "\tThank you for your kind donation of $ {:.2f}.\n"
                                          "\tIt will be put to very good use.\n"
                                          "\t\tSincerely,\n"
                                          "\t\t\t-The Team").format(
                            file_name.donor_name,
                            file_name.total_amount)
                        tf.write(letter_content)
                except FileNotFoundError as err:
                    print("File path is not correct.")
                    print(err)
            print("Done")

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def add_a_donor(self):
        """Prompts for the name of new donor to be added"""
        donor_name = input("Please enter a name for the new donor: ")
        donor_location = input("Please enter a locations for your donor: ")
        self.add_donor(donor_name, donor_location)

    def delete_a_donor(self):
        """Prompts for the name of the donor to be deleted"""
        donor_name = input("Please enter a name for the new donor: ")
        self.delete_donor(donor_name)

    def add_a_donation(self):
        """Prompts for a name and donation amont to be added"""
        donor_name = input("Please enter the name of the donor: ")

        while True:
            try:
                donation_amount = float(input("Please enter a positive number "
                                              "for your "
                                              "donation "))
                if donation_amount > 0:
                    break
                else:
                    print('Number must be positive: ')
            except ValueError:
                print('Input must be a number')
        self.add_donation(donor_name, donation_amount)


    def update_donor(self):
        """Prompts for the current name of a donor and the new name to be
        updated"""
        old_donor_name = input("Please enter the name of the donor you need "
                               "to update: ")
        new_donor_name = input("Please enter the name you want to update to: ")
        self.update_donor_name(old_donor_name, new_donor_name)


actions_dictionary = {'1': 'Quit',
                      '2': 'Create a Report',
                      '3': 'Send letters to everyone',
                      '4': 'Send a Thank You',
                      '5': 'Add a donor',
                      '6': 'Add a donation',
                      '7': 'Delete a donor',
                      '8': 'Print full list of donors',
                      '9': 'Update donor name',
                      '10': 'Print only donor names'}


def select_action_dictionary(prompt, switch_func_dict):
    """User selects an action by its corresponding order number."""
    while True:
        choice_actions = input(prompt)
        try:
            if switch_func_dict[choice_actions]() == "quit":
                print("Before quitting.")
                break
        except KeyError:
            print("Please enter only one of the listed options.")


def print_menu():
    """Prints the action list to the console"""
    str_result = ''
    for i in actions_dictionary:
        str_result += ("{}) {}".format(i, actions_dictionary[i]))
        str_result += '\n'
    str_result += 'Select the corresponding number for the action you want to take action: '
    return str_result


def calculate_date():
    """Calculated todays date and reurns a string"""
    today_date = datetime.datetime.now()
    result_today_date = "_" + str(today_date.year) + "_" + str(
        today_date.month) + "_" + str(today_date.day)
    return result_today_date


def quit_program():
    """Quits the program."""
    return "quit"


myDB = DonorDB(SqliteDatabase('donor_list.db'))

switch_func_dict = {
    '1': quit_program,
    '2': myDB.calculate_report,
    '3': myDB.send_everyone_letters,
    '4': myDB.sending_thank_you,
    '5': myDB.add_a_donor,
    '6': myDB.add_a_donation,
    '7': myDB.delete_a_donor,
    '8': myDB.print_db,
    '9': myDB.update_donor,
    '10': myDB.print_only_donors
}

if __name__ == '__main__':
    select_action_dictionary(print_menu(), switch_func_dict)
