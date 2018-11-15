'''
Shin Tran
Python 220
Lesson 7 Assignment
'''

#!/usr/bin/env python3
# Implementing the mailroom program using a database connection


from create_donor_db import *
from decimal import Decimal
from peewee import *
from pprint import pprint as pp
import logging
import sqlite3
import sys


def get_email_text(current_donation):
    """Prints a thank you email to a donator
    Donor name and amount is passed in as a parameter"""
    return "Dear {:s},\n\
        Thank you for the generous donation of ${:,.2f}.\n\
        Sincerely,\n\
        Your Local Charity".format(*current_donation)


def generate_name_list():
    """Creates a list of all the distinct donors, returns a list
    helper method for print_names"""
    
    database = SqliteDatabase('mailroom.db')
    donor_list  = []
    try:
        logger.info("Connecting to DB, to print the Donor records")
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in Donor.select():
            donor_list.append(donor.full_name)
    except Exception as e:
        logger.error("Can't print donor names")
        logger.info(e)
    finally:
        database.close()
    return list(donor_list)


def print_names():
    """Prints out all the names in the name list,
    references generate_name_list"""
    for name in generate_name_list():
        print(name)


def add_donation():
    """Prompts the user to type a name of a donor, enter a donation amount,
    prints an email thanking the donor
    If the user types exit, it would return to the main prompt"""
    temp_list = []
    donor_name = get_new_donor_name()
    if (donor_name != 'exit'):
        temp_list.append(donor_name)
        donation_amt = get_new_donor_amount()
        if (donation_amt != 'exit'):
            temp_list.append(float(donation_amt))
            logger.info("{} has donated {}".format(*temp_list))
            database = SqliteDatabase('mailroom.db')
            try:
                logger.info("Connecting to DB, to add to the Donor records")
                database.connect()
                database.execute_sql('PRAGMA foreign_keys = ON;')
                if donor_name in generate_name_list():
                    donor_info = Donor.select().where(Donor.full_name == donor_name)
                    for item in donor_info:
                        update_donor = (Donor
                            .update(donation_count = item.donation_count + 1,
                                total_donation = item.total_donation + Decimal(temp_list[1]))
                            .where(Donor.full_name == temp_list[0]))
                        update_donor.execute()
                else:
                    new_donor = (Donor.insert(
                        full_name = temp_list[0],
                        donation_count = 1,
                        total_donation = temp_list[1]))
                    new_donor.execute()
                new_dn = (Donations.insert(
                    full_name = temp_list[0],
                    donation = temp_list[1]))
                new_dn.execute()
                logger.info('Database add successful')
            except Exception as e:
                logger.error("Can't add new donation")
                logger.info(e)
            finally:
                database.close()
                print(get_email_text(temp_list))


def delete_donation():
    """Prints all the records in the Donations table,
    prompts the user to type a donation ID to delete,
    also updates the Donor table accordingly"""
    database = SqliteDatabase('mailroom.db')
    try:
        logger.info("Connecting to DB, to delete a Donor record")
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        print_donations()
        del_record = get_donation_ID('d')
        del_query = Donations.select().where(Donations.id == int(del_record))
        temp_list = []
        for item in del_query:
            temp_list.append(item.full_name)
            temp_list.append(item.donation)
            delete_dn = (Donations.delete().where(Donations.id == int(del_record)))
            delete_dn.execute()
        logger.info('Updating Donor table so it matches the Donations table')
        update_donor = (Donor.select().where(Donor.full_name == temp_list[0]))
        for item in update_donor:
            updated_rec = (Donor
                .update(donation_count = item.donation_count - 1,
                    total_donation = item.total_donation - Decimal(temp_list[1]))
                .where(Donor.full_name == temp_list[0]))
            updated_rec.execute()
        logger.info('Database delete successful')
    except Exception as e:
        logger.error("Can't delete the donation")
        logger.info(e)
    finally:
        database.close()


def update_donation():
    """Prompts the user to type a donation ID to delete,
    also updates the Donor table accordingly"""
    database = SqliteDatabase('mailroom.db')
    try:
        logger.info("Connecting to DB, to delete a Donor record")
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        print_donations()
        upd_record = get_donation_ID('u')
        new_dn_amt = get_new_donor_amount()
        if float(new_dn_amt) <= 0:
            print("Invald input:")
            new_dn_amt = get_new_donor_amount()
        upd_query = Donations.select().where(Donations.id == int(upd_record))
        temp_list = []
        for item in upd_query:
            temp_list.append(item.full_name)
            temp_list.append(item.donation)
            update_dn = (Donations
                .update(donation = Decimal(new_dn_amt))
                .where(Donations.id == int(upd_record)))
            update_dn.execute()
        logger.info('Going through the donations table to get')
        logger.info('total cumulative donation for a donor')
        temp_sum = 0
        new_sum = (Donations.select()
            .where(Donations.full_name == temp_list[0]))
        for item in new_sum:
            temp_sum += item.donation
        updated_rec = (Donor
            .update(total_donation = temp_sum)
            .where(Donor.full_name == temp_list[0]))
        updated_rec.execute()

        logger.info('Database udpate successful')
    except Exception as e:
        logger.error("Can't update the donation")
        logger.info(e)
    finally:
        database.close()


def print_donations():
    """Connects to the database Donations table,
    prints out every record"""
    database = SqliteDatabase('mailroom.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Donations.select())
        pp("   ID | Donor Name           | Donation")
        pp("---------------------------------------")
        for item in query:
            pp("{:5} | {:20} | {:8}".format(item.id, str(item.full_name), item.donation))
        print()
    except Exception as e:
        logger.error("Can't print the donations")
        logger.info(e)
    finally:
        database.close()


def send_letters():
    """Goes through all the previous donators, gets their total donated,
    sends a thank you letter that is output on a .txt file"""
    message = "Dear {:s},\n\
    Thank you for donating ${:,.2f}.\n\
    Sincerely,\n\
    Your Local Charity"
    database = SqliteDatabase('mailroom.db')
    try:
        logger.info("Connecting to DB, to print the individual Donor record")
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = Donor.select()
        for item in query:
            with open(item.full_name + ".txt",'w') as output:
                output.write(message.format(item.full_name, item.total_donation))
    except Exception as e:
        logger.error("Can't write to text document")
        logger.info(e)
    finally:
        database.close()
    print("Letters have been generated.")


def generate_report():
    """Generates a report of all the previous donators
    Report includes name, total donated, count of donations, average gift
    Report is also formatted with a certain spacing
    returns the report as a string"""
    donation_total = []
    database = SqliteDatabase('mailroom.db')
    try:
        logger.info("Connecting to DB, to print all the Donor records for report.")
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = Donor.select().where(Donor.donation_count > 0)
        for item in query:
            donation_total.append(
                [item.full_name,
                item.total_donation,
                item.donation_count,
                item.total_donation/item.donation_count])
    except Exception as e:
        logger.error("Can't pull records from database")
        logger.info(e)
    finally:
        database.close()
    donation_total.sort(key=lambda l: l[1], reverse = True)
    s1 = "Donor Name          |   Total Given  |  Num Gifts |  Average Gift\n"
    s2 = "-----------------------------------------------------------------\n"
    final_string = s1 + s2
    for z in range(0, len(donation_total)):
        s3 = '{:20} ${:13,.2f}{:14}  ${:13,.2f}\n'.format(*donation_total[z])
        final_string += s3
    return final_string


def print_report():
    """Prints a report of all the previous donators references generate_report"""
    print(generate_report())


def main_prompt():
    """Prompts the user to enter an option"""
    response = input("\n\
        Choose from one of 4 actions:\n\
        1) Add a Donation\n\
        2) Delete a Donation\n\
        3) Update a Donation\n\
        4) Create a Report\n\
        5) Send letters to everyone\n\
        0) Quit\n\
        Please type 1, 2, 3, 4, 5, or 0: ")
    return response

def action(switch_dict):
    """Takes in a user input as a parameter, enters a donation, prints a report,
    prints list, exit, prompts again if the input is bad
    If the user types exit it'll go back to the main prompt"""
    while True:
        user_input = main_prompt()
        try:
            switch_dict.get(user_input)()
        except (TypeError, ValueError):
            print("Invalid input, {} please try again.".format(user_input))

def get_new_donor_name():
    """Prompts the user for a new donor name"""
    return input("Enter a full name: ")

def get_new_donor_amount():
    """Prompts the user for a donation amount"""
    return input("Enter a donation amount: ")

def get_donation_ID(upd_or_del):
    """Prompts the user for a donation ID"""
    if upd_or_del == 'd':
        return input("Enter a donation ID to delete: ")
    else:
        return input("Enter a donation ID to update: ")

# Python program to use main for function call
if __name__ == "__main__":
    switch_dict = {
        'list': print_names,
        '1': add_donation,
        '2': delete_donation,
        '3': update_donation,
        '4': print_report,
        '5': send_letters,
        '0': sys.exit
    }
    action(switch_dict)
