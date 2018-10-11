#!/usr/bin/env python3

import configparser
from pathlib import Path
import pymongo
import utilities
import login_database

log = utilities.configure_logger('default', 'logs/mongodb_script.log')

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

prompt = ("\nWhat would you like to do?\n"
          "Choose an action from this list:\n"
          "1 - Add a New Donation\n"
          "2 - Send a Thank You\n"
          "3 - Thank Everyone\n"
          "4 - Create a Report\n"
          "5 - Update an Entry\n"
          "6 - Delete an Entry\n"
          "7 - Quit\n")

donations = [
        {
            'donor': 'Ted Laws',
            'donation_amt': 1000
        },
        {
            'donor': 'Ted Laws',
            'donation_amt': 100
        },
        {
            'donor': 'Kristin Laws',
            'donation_amt': 150
        },
        {
            'donor': 'Ryan Moore',
            'donation_amt': 600
        },
        {
            'donor': 'Beth Ross',
            'donation_amt': 1000
        },
        {
            'donor': 'Andrew Crawford',
            'donation_amt': 2000
        },
        {
            'donor': 'Andrew Crawford',
            'donation_amt': 4000
        },
        {
            'donor': 'Andrew Crawford',
            'donation_amt': 2000
        }]


def menu_selection(prompt, dispatch_dict, client, database):
    """
        give the user a menu to choose from
    """
    while True:
        response = input(prompt)
        try:
            if dispatch_dict[response](client, database) == "Exit Menu":
                break
        except KeyError:
            print("\nThat was not one of the options.")


def exit(client, database):
    """
        exit the program
    """
    return "Exit Menu"


def number_collector(prompt):
    """
        make sure that the user inputs an integer
    """
    while True:
        try:
            output = int(input(prompt))
            break
        except ValueError:
            print("\nThat wasn't a number value.")
    return output


def add_new_donation(client, database):
    """
        add a new donation to the database
    """
    name = input("\nA new donation! Who donated? (First and Last Name): ")

    query = {'donor': name}
    results = database.find_one(query)

    if results:
        print("A return donor!")

    amount = number_collector("\nHow much did {} donate: ".format(name))

    new_donation = {'donor': name, 'donation_amt': amount}
    database.insert_one(new_donation)


def donor_totals(name, client, database):
    """
        get donation and donation amount totals for a given donor
    """

    query = {'donor': name}
    results = database.find(query)
    total_donated = 0
    total_donations = 0

    if results:
        for donation in results:
            total_donated += donation['donation_amt']
            total_donations += 1
        return total_donations, total_donated
    else:
        print('You requested a report for someone who has never donated.')
        return (0, 0)


def write_thank_you(client, database, name=""):
    """
        write a thank you note
    """

    if name == "":
        name = input("\nWho would you like a thank you note for? "
                     "(First and Last Name): ")

    total_donations, total_donated = donor_totals(name, client, database)

    if total_donations > 0:
        note = ("Dear {},\n"
                "\nThank you for your generosity to our cause.\n"
                "You have now given {} time(s) for a total of ${:,}."
                "\nWe greatly appreciate your contributions!"
                "\n\nThank you!\nAlex Laws".format(name,
                                                   total_donations,
                                                   total_donated))
        with open("{}.txt".format(name), 'w') as f:
            f.write(note)
    else:
        print("That person has not made any donations.")


def thank_everyone(client, database):
    """
        write a thank you note for everyone
    """

    all_donors = database.distinct('donor')

    for donor in all_donors:
        write_thank_you(client, database, donor)


def build_report(client, database):
    """
        build a report of donors and their donations
    """

    print("\n")
    print("Donor Name       |  Total Given  |  Num Gifts  |  Average Gift")

    all_donors = database.distinct('donor')

    for donor in all_donors:
        total_donations, total_donated = donor_totals(donor, client, database)
        avg = total_donated / total_donations
        print("{:17} ${:14,.2f} {:13} ${:13,.2f}".format(donor,
                                                         total_donated,
                                                         total_donations,
                                                         avg))


def update_donor(name, client, database):
    """
        update a donor's name
    """
    full_name = input("What is the correct name: ")
    database.update_many(
        {'donor': name},
        {'$set': {'donor': full_name}})
    return full_name


def update_donation(name, client, database):
    """
        update a single donation
    """
    query = {'donor': name}
    results = database.find(query)
    print("Here are the donations for {}:".format(name))
    for donation in results:
        print('${:.2f}'.format(donation['donation_amt']))
    gift_to_update = number_collector("Which donation amount would you like to update: ")
    correct_amt = number_collector("How much is the actual donation: ")
    database.update_one(
        {'$and': [{'donor': name}, {'donation_amt': gift_to_update}]},
        {'$set': {'donation_amt': correct_amt}})


def delete_donation(name, client, database):
    """
        delete a single donation
    """
    query = {'donor': name}
    results = database.find(query)
    print("Here are the donations for {}:".format(name))
    for donation in results:
        print('${:.2f}'.format(donation['donation_amt']))
    gift_to_delete = number_collector("Which donation amount do you need to delete: ")
    database.delete_one(
        {'$and': [{'donor': name}, {'donation_amt': gift_to_delete}]})


def update_entry(client, database):
    """
        choose the entry to update
    """

    which_donor = input("Which Donor account do you want to update: ")

    query = {'donor': which_donor}
    donor_entry = database.find_one(query)

    if donor_entry:
        what_update = input("Do you want to update a donation or the donor "
                            "record (enter Donor, Donation, or both): ")
        if what_update == "Donor":
            update_donor(donor_entry['donor'], client, database)
        elif what_update == "Donation":
            update_donation(donor_entry['donor'], client, database)
        elif what_update == "Both":
            new_name = update_donor(donor_entry['donor'], client, database)
            update_donation(new_name, client, database)
        else:
            print("Please select an option. Try again.")
    else:
        print('That person is not in our records. Please add a new entry.')


def delete_entry(client, database):
    """
        choose the entry to delete
    """

    which_donor = input("Which Donor account contains the entry "
                        "you need to delete: ")

    query = {'donor': which_donor}
    donor_entry = database.find_one(query)

    if donor_entry:
        what_delete = input("Do you want to delete a donation or the entire "
                            "donor record (enter Donor or Donation): ")
        if what_delete == "Donor":
            database.remove({'donor': which_donor})
        elif what_delete == "Donation":
            delete_donation(donor_entry['donor'], client, database)
        else:
            print("Please select an option. Try again.")
    else:
        print('That person is not in our records. No need to delete.')


menu_dict = {"1": add_new_donation, "2": write_thank_you,
             "3": thank_everyone, "4": build_report,
             "5": update_entry, "6": delete_entry, "7": exit}

if __name__ == '__main__':
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        donation_db = db['donation_db']
        donation_db.insert_many(donations)
        menu_selection(prompt, menu_dict, client, donation_db)
        db.drop_collection('donation_db')
