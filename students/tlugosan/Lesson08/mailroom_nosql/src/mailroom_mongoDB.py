#!/usr/bin/env python3
""" Automate a script to send a thank you mail, print a report of donor or quit the program."""
from operator import itemgetter
import os
import datetime
import login_database
import utilities
import learn_data

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def mongoDB1():
    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called dev')
        db = client['dev']

        log.info('And in that database use a collection called donor_list')
        donor_list = db['donor_list']
        log.info('Step 2: Delete the collection so we can start from scratch')
        donor_list.delete_many({})
        donor_data = learn_data.get_donor_data()

        log.info(
            'Step 2: Now we add data from the dictionary that extracted from the learn_data file')
        donor_list.insert_many(donor_data)

        return donor_list


class DonorDB:
    def __init__(self, database):
        self.database = database

    def print_all(self):
        all_donors = self.find_all_donors()
        for obj in all_donors:
            # pprint.pprint(obj)
            print(obj['name'] + ' lives in ' +
                  obj['lives_in'] + ' donated the following amounts: [', end = '')
            donation_list = obj['donations']
            for obd in range(0, len(donation_list)):
                if obd < (len(donation_list) - 1):
                    print(str(obj['donations'][obd]) + ", ", end='')
                else:
                    print(str(obj['donations'][obd]), end='')
            print(']')
        print(all_donors.count())

    def print_only_donors(self):
        all_donors = self.find_all_donors()
        for obj in all_donors:
            print(obj['name'])

    def add_donor(self, person_name, lives_in):
        """Adds a donor only to the Donor table"""
        add_donor_query = self.database.insert_one({'name': person_name,
                                                    'lives_in': lives_in,
                                                    'donations': []})

    def delete_donor(self, person_name):
        """Deletes a donor entireley from the database and any reference of
        it"""
        delete_donor_query = self.database.delete_one({'name': person_name})

    def add_donation(self, donor_name, donation_amount):
        find_donor_query = {'name': donor_name}
        new_value = {'$push': {'donations': donation_amount}}
        add_donation_query = self.database.update_one(find_donor_query,
                                                      new_value)

    def update_donor_name(self, old_name, new_name):
        find_donor_query = {'name': old_name}
        new_value = {'$set': {'name': new_name}}
        update_donor_name = self.database.update(find_donor_query, new_value)

    def calculate_report(self):
        table_header = ['Donor Name', 'Total Given', 'Num Gifts',
                        'Average Gifts']
        len_header = len(table_header)
        print("|".join(["{:<20}"] * len_header).format(*table_header))
        print("-" * (20 * len_header + (len_header - 1)))

        all_donors = self.find_all_donors()

        for d in all_donors:
            total_amount_per_donor = sum(d['donations'])
            number_donations_per_donor = len(d['donations'])
            average_donation = total_amount_per_donor / number_donations_per_donor
            print("{:<20}| ${:<19}| {:<19}| ${:<19}".format(d['name'],
                                                            str(round(
                                                                total_amount_per_donor,
                                                                2)),
                                                            number_donations_per_donor,
                                                            str(round(
                                                                average_donation,
                                                                2))))

    def find_all_donors(self):
        all_donors = self.database.find()
        return all_donors

    def sending_thank_you(self):

        """Lists all the donors or prompts for a name and donation amount to compile the thank you email."""
        self.print_all()
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

        aperson = self.database.find_one(
            {'name': donor_name, 'donations': donation_amount})
        if aperson == None:
            print('Person or affiliated amount doesn\'t exist in the '
                  'database')
        else:
            print(
                "Dear {}, Thank you for your generous contribution of ${:.2f} "
                "to our program.".format(donor_name,
                                         donation_amount))

    def send_everyone_letters(self, target_directory=os.getcwd()):
        """Sends a letter to everyone in the table for their first donation in the list."""
        file_name_extension = '.txt'
        today_date_short = calculate_date()
        all_donors = self.find_all_donors()

        for file_name in all_donors:
            target_file_path = os.path.join(target_directory,
                                            str(
                                                file_name['name']).replace(
                                                ' ',
                                                '_') + today_date_short + file_name_extension)
            try:
                total_amount_per_donor = sum(file_name['donations'])
                with open(str(target_file_path), 'w') as tf:
                    letter_content = ("Dear {},\n"
                                      "\tThank you for your kind donation of $ {:.2f}.\n"
                                      "\tIt will be put to very good use.\n"
                                      "\t\tSincerely,\n"
                                      "\t\t\t-The Team").format(
                        file_name['name'],
                        total_amount_per_donor)
                    tf.write(letter_content)
            except FileNotFoundError as err:
                print("File path is not correct.")
                print(err)
        print("Done")

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


myDB = DonorDB(mongoDB1())

switch_func_dict = {
    '1': quit_program,
    '2': myDB.calculate_report,
    '3': myDB.send_everyone_letters,
    '4': myDB.sending_thank_you,
    '5': myDB.add_a_donor,
    '6': myDB.add_a_donation,
    '7': myDB.delete_a_donor,
    '8': myDB.print_all,
    '9': myDB.update_donor,
    '10': myDB.print_only_donors
}

if __name__ == '__main__':
    select_action_dictionary(print_menu(), switch_func_dict)
    # myDB = DonorDB(mongoDB1())
    # myDB.print_all()
    # myDB.add_donor("Beth", "something")
    # myDB.print_all()
    # myDB.delete_donor("Toni Orlando")
    # myDB.print_all()
    # myDB.add_donation("Beth", 333)
    # myDB.print_all()
    # myDB.update_donor_name("Beth", "Jimmy")
    # myDB.print_all()
    # myDB.calculate_report()
    # myDB.sending_thank_you()
    # myDB.send_everyone_letters()
