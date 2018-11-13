'''
Shin Tran
Python 220
Lesson 7 Assignment
'''

#!/usr/bin/env python3
# Implementing the mailroom program using a database connection


from peewee import *
from create_donor_db import *
import logging
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


def send_thanks():
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
            try:
                logger.info("Connecting to DB, to add or upddate the Donor records")
                database.connect()
                database.execute_sql('PRAGMA foreign_keys = ON;')
                with database.transaction():
                    new_dn = (Donations.insert(
                        full_name = temp_list[0],
                        donation = temp_list[1]).execute())
                    new_dn.save()
                    logger.info('Database add successful')
                if donor_name in Donor.select():
                    dn_count = Donor.select(Donor.donation_count + 1).where(Donor.full_name == temp_list[0])
                    total_dn = Donor.select(Donor.total_donation + temp_list[1]).where(Donor.full_name == temp_list[0])
                    print("does it go here? " + dn_count + " " + total_dn)
                    update_donor = (Donor
                        .update(donation_count = dn_count, donation_total = total_dn)
                        .where(Donor.full_name == temp_list[0]).execute())
                    update_donor.save()
                else:
                    with database.transaction():
                        new_donor = (Donor.insert(
                            full_name = temp_list[0],
                            donation_count = 1,
                            total_donation = temp_list[1]).execute())
                        new_donor.save()
                    logger.info('Database add successful')
            except Exception as e:
                logger.error("Can't add new donation")
                logger.info(e)
            finally:
                database.close()
                print(get_email_text(temp_list))


def send_letters():
    """Goes through all the previous donators, gets their total donated,
    sends a thank you letter that is output on a .txt file"""
    message = "Dear {:s},\n\
    Thank you for donating ${:,.2f}.\n\
    Sincerely,\n\
    Your Local Charity"
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
    try:
        logger.info("Connecting to DB, to print all the Donor records for report.")
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = Donor.select()
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
        1) Send a Thank You\n\
        2) Create a Report\n\
        3) Send letters to everyone\n\
        0) Quit\n\
        Please type 1, 2, 3, or 0: ")
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

# Python program to use main for function call
if __name__ == "__main__":
    switch_dict = {
        'list': print_names,
        '1': send_thanks,
        '2': print_report,
        '3': send_letters,
        '0': sys.exit
    }
    action(switch_dict)
