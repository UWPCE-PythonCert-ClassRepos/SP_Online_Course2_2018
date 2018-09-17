#!/usr/bin/env python3

import configparser
from pathlib import Path
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

email = 0
city = 1
donor_type = 2
donor_id = 3

donor_ids = [1, 2, 3, 4, 5]


def populate_db(db):
    """
        populate the redis database
    """
    db.rpush('Ted Laws', 'ted.laws@email.com')
    db.rpush('Ted Laws', 'Philadelphia')
    db.rpush('Ted Laws', 'Family')
    db.rpush('Ted Laws', 1)
    db.rpush('Ted Laws', 1000)
    db.rpush('Ted Laws', 100)

    db.rpush('Kristin Laws', 'kristin.laws@email.com')
    db.rpush('Kristin Laws', 'Philadelphia')
    db.rpush('Kristin Laws', 'Family')
    db.rpush('Kristin Laws', 2)
    db.rpush('Kristin Laws', 150)

    db.rpush('Ryan Moore', 'Ryan.Moore@email.com')
    db.rpush('Ryan Moore', 'New York')
    db.rpush('Ryan Moore', 'Friend')
    db.rpush('Ryan Moore', 3)
    db.rpush('Ryan Moore', 600)

    db.rpush('Beth Ross', 'beth.ross@email.com')
    db.rpush('Beth Ross', 'Ann Arbor')
    db.rpush('Beth Ross', 'Family')
    db.rpush('Beth Ross', 4)
    db.rpush('Beth Ross', 1000)

    db.rpush('Andrew Crawford', 'Andrew.crawford@email.com')
    db.rpush('Andrew Crawford', 'Washington, DC')
    db.rpush('Andrew Crawford', 'Family')
    db.rpush('Andrew Crawford', 5)
    db.rpush('Andrew Crawford', 2000)
    db.rpush('Andrew Crawford', 2000)
    db.rpush('Andrew Crawford', 4000)

    db.set(1, 'Ted Laws')
    db.set(2, 'Kristin Laws')
    db.set(3, 'Ryan Moore')
    db.set(4, 'Beth Ross')
    db.set(5, 'Andrew Crawford')

    db.set('Total Donors', 5)


def menu_selection(prompt, dispatch_dict, database):
    """
        give the user a menu to choose from
    """
    while True:
        response = input(prompt)
        try:
            if dispatch_dict[response](database) == "Exit Menu":
                break
        except KeyError:
            print("\nThat was not one of the options.")


def exit(db):
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


def add_new_donation(db):
    """
        add a new donation to the database, along with key information
    """
    name = input("\nA new donation! Who donated? (First and Last Name): ")
    amount = number_collector("\nHow much did {} donate: ".format(name))

    if db.llen(name) > 0:
        print("They're a return donor!")
        db.rpush(name, amount)
    else:
        print("Let's get some information about {}.".format(name))
        db.rpush(name, input("Email: "))
        db.rpush(name, input("City: "))
        db.rpush(name, input("Relationship: "))
        db.incr('Total Donors')
        db.rpush(name, int(db.get('Total Donors')))
        db.rpush(name, amount)
        db.set(db.get('Total Donors'), name)
        donor_ids.append(int(db.get('Total Donors')))


def donor_totals(name, db):
    """
        get donation and donation amount totals for a given donor
    """
    total_donations = int(db.llen(name)) - 4
    total_donated = 0

    for x in range(total_donations):
        total_donated += int(db.lindex(name, x + 4))
    return total_donations, total_donated


def write_thank_you(db, name=""):
    """
        write a thank you note
    """

    if name == "":
        name = input("\nWho would you like a thank you note for? "
                     "(First and Last Name): ")

    total_donations, total_donated = donor_totals(name, db)

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


def thank_everyone(db):
    """
        write a thank you note for everyone
    """

    for x in range(int(db.get('Total Donors'))):
        write_thank_you(db, db.get(x + 1))


def build_report(db):
    """
        build a report of donors and their donations
    """

    print("\n")
    print("Donor Name       |  Total Given  |  Num Gifts  |  Average Gift")

    for donor_id in donor_ids:
        donor = r.get(donor_id)
        total_donations, total_donated = donor_totals(donor, db)
        avg = total_donated / total_donations
        print("{:17} ${:14,.2f} {:13} ${:13,.2f}".format(donor,
                                                         total_donated,
                                                         total_donations,
                                                         avg))


def update_donor(name, db):
    """
        update a donor's name
    """
    full_name = input("What is the correct name: ")
    for x in range(int(db.llen(name))):
        db.rpush(full_name, db.lpop(name))
    db.set(db.lindex(full_name, donor_id), full_name)
    return full_name


def update_donation(name, db):
    """
        update a single donation
    """
    print("Here are the donations for {}:".format(name))
    for x in range(4, db.llen(name)):
        print('{}. ${:.2f}'.format(x - 3, int(db.lindex(name, x))))
    gift_to_update = number_collector("Which donation number would you like to update: ")
    correct_amt = number_collector("How much is the actual donation: ")
    db.lset(name, gift_to_update + 3, correct_amt)


def delete_donation(name, db):
    """
        delete a single donation
    """
    print("Here are the donations for {}:".format(name))
    for x in range(4, db.llen(name)):
        print('{}. ${:.2f}'.format(x - 3, int(db.lindex(name, x))))
    gift_to_delete = number_collector("Which donation number would you like to delete: ")
    db.lset(name, gift_to_delete + 3, -1)
    db.lrem(name, 0, -1)


def update_entry(db):
    """
        choose the entry to update
    """

    which_donor = input("Which Donor account do you want to update: ")

    if db.llen(which_donor) > 0:
        what_update = input("Do you want to update a donation or the donor "
                            "record (enter Donor, Donation, or Both): ")
        if what_update == "Donor":
            update_donor(which_donor, db)
        elif what_update == "Donation":
            update_donation(which_donor, db)
        elif what_update == "Both":
            new_name = update_donor(which_donor, db)
            update_donation(new_name, db)
        else:
            print("Please select an option. Try again.")
    else:
        print('That person is not in our records. Please add a new entry.')


def delete_entry(db):
    """
        choose the entry to delete
    """
    which_donor = input("Which donor account do you want to manage: ")

    if db.llen(which_donor) > 0:
        what_delete = input("Do you want to delete a donation or the entire "
                            "donor record (enter Donor or Donation): ")
        if what_delete == "Donor":
            db.delete(db.lindex(which_donor, donor_id))
            donor_ids.remove(int(db.lindex(which_donor, donor_id)))
            db.ltrim(which_donor, int(db.llen(which_donor)) + 1, int(db.llen(which_donor)) + 2)
        elif what_delete == "Donation":
            delete_donation(which_donor, db)
        else:
            print("Please select an option. Try again.")
    else:
        print('That person is not in our records. No need to delete.')


menu_dict = {"1": add_new_donation, "2": write_thank_you,
             "3": thank_everyone, "4": build_report,
             "5": update_entry, "6": delete_entry, "7": exit}

if __name__ == '__main__':
    r = login_database.login_redis_cloud()
    r.flushdb()
    populate_db(r)
    menu_selection(prompt, menu_dict, r)
