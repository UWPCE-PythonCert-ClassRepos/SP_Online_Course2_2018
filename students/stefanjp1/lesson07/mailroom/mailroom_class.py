""" Module to run user interface to mailroom database """

import sys
from peewee import *
from db_model import *


def donor_totals(name):
    """ Return the count and sum of donations for a donor """
    all_donation_records = Donation_Records.select().where(Donation_Records.donor == name)

    total_donated = 0
    total_donations = 0
    for donation in all_donation_records:
        total_donated += donation.donation_amt
        total_donations += 1

    return total_donations, total_donated


def add_new_donation():
    """ add a new donation to the database """
    name = input("Enter the donor's full name > ")

    try:
        donor = Donor_Records.get(Donor_Records.donor_name == name)
    except:
        donor = Donor_Records.create(donor_name=name)

    amount = float(input("\nEnter donation amount: "))

    new_donation = Donation_Records.create(donor=name,
                                           donation_amt=amount)
    new_donation.save()
    return name


def send_thank_you(name='add_donation'):
    """ Print or return a stock thank you letter """
    if name == 'add_donation':
        name = add_new_donation()
        total_donations, total_donated = donor_totals(name)

        print("""Dear {},\n\n\tThank you for your kind donations totaling ${:.2f}.\n\n\t
        It will go a long way to feed the needy. \n\n\t\tSincerely, \n\n\t\t  -The Team""".format(name, total_donated))
    else:
        total_donations, total_donated = donor_totals(name)

        return"""Dear {},\n\n\tThank you for your kind donations totaling ${:.2f}.\n\n\t
        It will go a long way to feed the needy. \n\n\t\tSincerely, \n\n\t\t  -The Team""".format(name, total_donated)


def send_letters():
    """ Create stock thank you letters for each donor """
    all_donors = Donor_Records.select(Donor_Records.donor_name)

    for donor in all_donors:
        name = donor.donor_name

        letter = send_thank_you(name)

        file_path = name + '.txt'
        with open(file_path, 'w') as outfile:
            outfile.write(letter)


def delete_donor():
    """ Remove a donor and his/her donations from the DB """
    name = input("Enter the donor's full name > ")

    Donation_Records.delete().where(Donation_Records.donor == name).execute()
    Donor_Records.delete().where(Donor_Records.donor_name == name).execute()
    print("Deleted donor {}".format(name))


def delete_donation():
    """ Remove a specific donation from the DB """
    name = input("Enter the donor's full name > ")

    all_donations = Donation_Records.select().where(Donation_Records.donor == name)
    print("Here are the donations for {}:".format(name))
    for donation in all_donations:
        print("{}. ${:.2f}".format(donation, donation.donation_amt))
    delete_row = input("Enter the number on the left of the row you want to delete: ")
    Donation_Records.delete().where(Donation_Records.id == delete_row).execute()
    print('Row Deleted')


if __name__ == '__main__':
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    while True:
        prompt = input("""Enter:\n Send a Thank You (1)\n Send Letter to Everyone (2)\n Delete a donor (3)\n Delete a donation (4)\n or quit (5) > """)

        try:
            prompt = int(prompt)
        except ValueError:
            print("Input must be an integer, try again.")
            continue

        prompt_dict = {1: send_thank_you,
                       2: send_letters,
                       3: delete_donor,
                       4: delete_donation,
                       5: 'quitting program'}

        try:
            user_choice = prompt_dict[prompt]
        except KeyError:
            print("Input integer was outside range of choices, try again.")
            continue

        if prompt != 5:
            user_choice()
        else:
            print(user_choice)
            database.close()
            sys.exit()
