#!/usr/bin/env python3

from mailroom_db import *
import os
import logging

prompt = ("\nWhat would you like to do?\n"
          "Choose an action from this list:\n"
          "1 - Add a New Donation\n"
          "2 - Send a Thank You\n"
          "3 - Thank Everyone\n"
          "4 - Create a Report\n"
          "5 - Update an Entry\n"
          "6 - Delete an Entry\n"
          "7 - Quit\n")


def menu_selection(prompt, dispatch_dict):
    while True:
        response = input(prompt)
        try:
            if dispatch_dict[response]() == "Exit Menu":
                break
        except KeyError:
            print("\nThat was not one of the options.")


def exit():
    return "Exit Menu"


def number_collector(prompt):
    while True:
        try:
            output = int(input(prompt))
            break
        except ValueError:
            print("\nThat wasn't a number value.")
    return output


def populate_db():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('donation_records.db')

    donors = [('Ted Laws', [1000, 100]), ('Kristin Laws', [150]),
              ('Ryan Moore', [600]), ('Beth Ross', [1000]),
              ('Andrew Crawford', [2000, 4000, 2000])]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor, donations in donors:
            with database.transaction():
                new_donor = Donor_Records.create(full_name=donor)
                new_donor.save()
                logger.info('{} Donor add successful'.format(donor))
            for donation in donations:
                new_donation = Donation_Records.create(donor=new_donor,
                                                       donation_amt=donation)
                new_donation.save()
                logger.info('{} ${} added'.format(donor, donation))

        logger.info('Print the donor records we saved...')
        for donor in Donor_Records:
            logger.info(f'{donor.full_name} donated.')

        logger.info('Print the donation records we saved...')
        for donation in Donation_Records:
            logger.info(f'{donation.donor.full_name} donated '
                        f'{donation.donation_amt}.')

    except Exception as e:
        logger.info(f'Error on {donor}.')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def add_new_donation():

    database = SqliteDatabase('donation_records.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    name = input("\nA new donation! Who donated? (First and Last Name): ")

    try:
        donor = Donor_Records.get(Donor_Records.full_name == name)
        if donor:
            print("A return donor!")
    except:
        donor = Donor_Records.create(full_name=name)
        donor.save()

    amount = number_collector("\nHow much did {} donate: ".format(name))

    new_donation = Donation_Records.create(donor=donor,
                                           donation_amt=amount)
    new_donation.save()

    database.close()


def donor_totals(name):

    database = SqliteDatabase('donation_records.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    try:
        donor = Donor_Records.get(Donor_Records.full_name == name)
    except:
        print('You requested a report for someone who has never donated.')
        return (0, 0)
    else:
        all_donations = Donation_Records.select().where(Donation_Records.donor == donor)
        total_donated = 0
        total_donations = 0
        for donation in all_donations:
            total_donated += donation.donation_amt
            total_donations += 1
        return total_donations, total_donated

    database.close()

def write_thank_you(name=""):

    if name == "":
        name = input("\nWho would you like a thank you note for? "
                     "(First and Last Name): ")

    total_donations, total_donated = donor_totals(name)

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


def thank_everyone():

    database = SqliteDatabase('donation_records.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    all_donors = Donor_Records.select(Donor_Records.full_name)

    for donor in all_donors:
        write_thank_you(donor.full_name)

    database.close()


def build_report():

    print("\n")
    print("Donor Name       |  Total Given  |  Num Gifts  |  Average Gift")

    database = SqliteDatabase('donation_records.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    all_donors = Donor_Records.select(Donor_Records.full_name)

    for donor in all_donors:
        total_donations, total_donated = donor_totals(donor.full_name)
        avg = total_donated / total_donations
        print("{:17} ${:14,.2f} {:13} ${:13,.2f}".format(donor.full_name,
                                                         total_donated,
                                                         total_donations,
                                                         avg))

    database.close()


def update_donor(name):
    change = Donor_Records.update(full_name=input("What is the correct name: ")).where(Donor_Records.full_name == name).execute()


def update_donation(donor):
    all_donations = Donation_Records.select().where(Donation_Records.donor == donor)
    print("Here are the donations:")
    for donation in all_donations:
        print("{}. ${:,}".format(donation, donation.donation_amt))
    gift_to_update = number_collector("Which # donation "
                                      "would you like to update: ")
    correct_amt = number_collector("How much is the actual donation: ")
    change = Donation_Records.update(donation_amt=correct_amt).where(Donation_Records.id == gift_to_update).execute()


def delete_donor(name):
    donor_to_delete = Donor_Records.select(Donor_Records.id).where(Donor_Records.full_name == name)
    donation_to_delete = Donation_Records.select(Donation_Records.id).where(Donation_Records.donor_id.in_(donor_to_delete))
    Donation_Records.delete().where(Donation_Records.id.in_(donation_to_delete)).execute()
    Donor_Records.delete().where(Donor_Records.id.in_(donor_to_delete)).execute()


def delete_donation(donor):
    all_donations = Donation_Records.select().where(Donation_Records.donor == donor)
    print("Here are the donations:")
    for donation in all_donations:
        print("{}. ${:,}".format(donation, donation.donation_amt))
    gift_to_update = number_collector("Which # donation "
                                      "would you like to delete: ")
    Donation_Records.delete().where(Donation_Records.id == gift_to_update).execute()


def update_entry():

    which_donor = input("Which Donor account do you want to update: ")

    database = SqliteDatabase('donation_records.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    try:
        donor = Donor_Records.get(Donor_Records.full_name == which_donor)
    except:
        print('That person is not in our records. Please add a new entry.')
    else:
        what_update = input("Do you want to update a donation or the donor "
                            "record (enter Donor, Donation, or both): ")
        if what_update == "Donor":
            update_donor(donor.full_name)
        elif what_update == "Donation":
            update_donation(donor)
        elif what_update == "Both":
            update_donor(donor.full_name)
            update_donation(donor)
        else:
            print("Please select an option. Try again.")

    database.close()


def delete_entry():

    which_donor = input("Which Donor account contains the entry "
                        "you need to delete: ")

    database = SqliteDatabase('donation_records.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    try:
        donor = Donor_Records.get(Donor_Records.full_name == which_donor)
    except:
        print('That person is not in our records. No need to delete.')
    else:
        what_update = input("Do you want to delete a donation or the entire "
                            "donor record (enter Donor or Donation): ")
        if what_update == "Donor":
            delete_donor(donor.full_name)
        elif what_update == "Donation":
            delete_donation(donor)
        else:
            print("Please select an option. Try again.")

    database.close()


menu_dict = {"1": add_new_donation, "2": write_thank_you,
             "3": thank_everyone, "4": build_report,
             "5": update_entry, "6": delete_entry, "7": exit}

if __name__ == '__main__':
    populate_db()
    menu_selection(prompt, menu_dict)
