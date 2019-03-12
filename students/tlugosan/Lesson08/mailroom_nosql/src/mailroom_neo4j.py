#!/usr/bin/env python3
""" Automate a script to send a thank you mail, print a report of donor or quit the program."""
from operator import itemgetter
import os
import datetime
import logging
import login_database
import utilities
import learn_data

log = utilities.configure_logger('default', '../logs/neo4j_script.log')


class DonorDB:
    def __init__(self):
        pass

    def find_all_donors(self):
        cyph = """MATCH (p:Person)
                  RETURN p.name as name, p.donations as donations
                """
        result = session.run(cyph)
        return result

    def print_all(self):
        print("People in database:")
        result = self.find_all_donors()
        for record in result:
            print(record['name'], record['donations'])

    def only_donors(self):
        all_donors = self.find_all_donors()
        donor_list = []
        for name in all_donors:
            donor_list.append(name['name'])
        return donor_list

    def add_donor(self, person_name):
        """Adds a donor only to the Donor table"""
        cyph = "CREATE(n:Person {name:'%s', donations:'%s'})" % (
            person_name, [])
        session.run(cyph)

    def delete_donor(self, person_name):
        """Deletes a donor entireley from the database and any reference of
        it"""
        cyph = "MATCH(n:Person {name:'%s'})" \
               "DELETE n" \
               % (person_name)

        session.run(cyph)

    def add_donation(self, donor_name, donation_amount):
        find_donation_list = self.find_all_donors()
        new_donation_list = []
        found = False
        for record in find_donation_list:
            if record['name'] == donor_name:
                current_donation_list = record['donations']
                remove_brackets = current_donation_list[1:len(
                current_donation_list) - 1].split(',')
                for rec in remove_brackets:
                    new_donation_list.append(float(rec))
                new_donation_list.append(float(donation_amount))
                found = True
                break

        if found:
            cyph = "MATCH (n:Person {name:'%s'})" \
                   "SET n.donations = '%s'" \
                   % (donor_name, new_donation_list)
            session.run(cyph)
        else:
            print("No donor was found in db with that name")

    def update_donor_name(self, old_name, new_name):
        cyph = "MATCH (n:Person {name:'%s'})" \
               "SET n.name = '%s'" \
               "RETURN n" \
               % (old_name, new_name)
        session.run(cyph)

    def calculate_report(self):
        table_header = ['Donor Name', 'Total Given', 'Num Gifts',
                        'Average Gifts']
        len_header = len(table_header)
        print("|".join(["{:<20}"] * len_header).format(*table_header))
        print("-" * (20 * len_header + (len_header - 1)))
        all_donors = self.find_all_donors()

        for d in all_donors:
            current_donation_list = d['donations']
            remove_brackets = current_donation_list[1:len(
                current_donation_list) - 1].split(',')
            total_amount_per_donor = 0
            for r in remove_brackets:
                total_amount_per_donor += float(r)

            number_donations_per_donor = len(remove_brackets)
            average_donation = total_amount_per_donor / number_donations_per_donor
            print("{:<20}| ${:<19}| {:<19}| ${:<19}".format(d['name'],
                                                            str(round(
                                                                total_amount_per_donor,
                                                                2)),
                                                            number_donations_per_donor,
                                                            str(round(
                                                                average_donation,
                                                                2))))

    def sending_thank_you(self):

        """Lists all the donors or prompts for a name and donation amount to compile the thank you email."""
        self.print_all()
        donor_name = input("Please enter the name of the person to send "
                           "thank you note from the printed list: ")
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

        all_donors = self.find_all_donors()
        doesExist = False
        for d in all_donors:
            if donor_name == d['name'] and str(donation_amount) in d['donations']:
                doesExist = True
                break
        if doesExist:
             print(
                    "Dear {}, Thank you for your generous contribution of ${:.2f} "
                    "to our program.".format(donor_name,
                                             donation_amount))
        else:
            print('Person or affiliated amount doesn\'t exist in the '
                  'database')

    def send_everyone_letters(self, target_directory=os.getcwd()):
        """Sends a letter to everyone in the table for their first donation in the list."""
        file_name_extension = '.txt'
        today_date_short = calculate_date()
        all_donors = self.find_all_donors()

        for fn in all_donors:
            file_name = fn['name']
            target_file_path = os.path.join(target_directory,
                                            str(
                                                file_name).replace(
                                                ' ',
                                                '_') + today_date_short + file_name_extension)
            try:
                current_donation_list = fn['donations']
                remove_brackets = current_donation_list[1:len(
                current_donation_list) - 1].split(',')
                total_amount_per_donor = 0
                for r in remove_brackets:
                    total_amount_per_donor += float(r)

                with open(str(target_file_path), 'w') as tf:
                    letter_content = ("Dear {},\n"
                                      "\tThank you for your kind donation of $ {:.2f}.\n"
                                      "\tIt will be put to very good use.\n"
                                      "\t\tSincerely,\n"
                                      "\t\t\t-The Team").format(
                        file_name,
                        total_amount_per_donor)
                    tf.write(letter_content)
            except FileNotFoundError as err:
                print("File path is not correct.")
                print(err)
        print("Done")

    def add_a_donor(self):
        """Prompts for the name of new donor to be added"""
        donor_name = input("Please enter a name for the new donor: ")
        self.add_donor(donor_name)

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


myDB = DonorDB()

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
    '10': myDB.only_donors
}

if __name__ == '__main__':
    log.info('Step 1: First, clear the entire database, so we can start over')
    log.info("Running clear_all")

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add a few people")

    with driver.session() as session:

        log.info('Adding a few Person nodes')
        log.info('The cyph language is analagous to sql for neo4j')
        db_list = [('Toni Orlando', [150.00, 200.00, 100.00]),
                   ('Amanda Clark', [1800]),
                   ('Robin Hood', [1234.56, 4500.34, 765.28]),
                   ('Gina Travis', [75.00]),
                   ('Mark Johnson', [850.00, 20.14])
                   ]
        for name, donations in db_list:
            cyph = "CREATE(n:Person {name:'%s', " \
                   "donations:'%s'})" % (
                       name, donations)
            session.run(cyph)
        select_action_dictionary(print_menu(), switch_func_dict)
        # myDB.add_donor("beth")
        # myDB.print_all()
        # myDB.delete_donor("Robin Hood")
        # myDB.print_all()
        # myDB.add_donation("beth", 234)
        # myDB.print_all()
        # myDB.update_donor_name("beth", "joe")
        # myDB.print_all()
        # myDB.calculate_report()
        # myDB.sending_thank_you()
        # myDB.send_everyone_letters()
