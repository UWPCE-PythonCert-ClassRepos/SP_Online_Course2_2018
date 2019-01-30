# ------------------------------------------------- #
# Title: Lesson 8, NOSQL
# Dev:   Craig Morton
# Date:  1/15/2019
# Change Log: CraigM, 1/15/2018, NOSQL
# ------------------------------------------------- #

#!/usr/bin/env python3

from decimal import Decimal
from pprint import pprint as pp
import donor_data
import logging
import login_database
import pymongo
import utilities


log = utilities.configure_logger('default', '../logs/mongodb_script.log')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_name_list():
    """Returns a list of all Donors"""
    donor_list = []
    results = donor.find()
    for item in results:
        donor_list.append(item['full_name'])
    return list(donor_list)


def print_names():
    """Prints list of names from name list."""
    for name in generate_name_list():
        print(name)


def get_email(current_donation):
    """Prints donation thank you letter."""
    return "Dear {:s},\n\
        Thank you for the generous donation of ${:,.2f}.\n\
        Sincerely,\n\
        Your Local Charity".format(*current_donation)


def add_donation():
    """User prompt to add donation"""
    temp_list = []
    donor_name = get_donor_name()
    if (donor_name != 'exit'):
        temp_list.append(donor_name)
        donation_amt = get_new_donor_amount()
        if (donation_amt != 'exit'):
            temp_list.append(float(donation_amt))
            logger.info("{} has donated {}".format(*temp_list))
            logger.info("Connecting to DB, to add to the Donor records")
            if donor_name in generate_name_list():
                rcrd = donor.find_one({'full_name': donor_name})
                dn_list = rcrd['donations']
                dn_list.append(temp_list[1])
                donor.find_one_and_update(
                    {"_id": rcrd["_id"]},
                    {'$set': {
                        'donations': rcrd['donations'],
                        'donation_count': rcrd['donation_count'] + 1,
                        'total_donation': rcrd['total_donation'] + temp_list[1]
                    }}
                )
                print("Database has been updated.")
            else:
                new_donor = {
                    'full_name': temp_list[0],
                    'donation_count': 1,
                    'total_donation': temp_list[1],
                    'donations': [temp_list[1]]
                }
                donor.insert_one(new_donor)
            logger.info('Database add successful')
            print(get_email(temp_list))


def delete_donor():
    """Remove Donor from database"""
    logger.info("Connecting to DB, to delete a Donor record")
    donor_name = get_donor_name()
    if donor_name in generate_name_list():
        del_query = donor.delete_many({'full_name': donor_name})
    logger.info('Database delete successful')


def update_donor():
    """Update Donor data"""
    logger.info("Connecting to DB, to update a Donor record")
    donor_name = get_donor_name()
    if donor_name in generate_name_list():
        new_dn_list = []
        new_dn_amt = get_new_donor_amount()
        print("Type 'no' if you want to stop adding donations.")
        while (new_dn_amt != 'no'):
            if float(new_dn_amt) <= 0:
                print("Invald input.")
            else:
               new_dn_list.append(float(new_dn_amt))
            new_dn_amt = get_new_donor_amount()
        if len(new_dn_list) != 0:
            rcrd = donor.find_one({'full_name': donor_name})
            donor.find_one_and_update(
                {"_id": rcrd["_id"]},
                {'$set': {
                    'donations': new_dn_list,
                    'donation_count': len(new_dn_list),
                    'total_donation': sum(new_dn_list)
                }}
            )
            logger.info('Database udpate successful')
    else:
        print("Name not found.")


def send_letters():
    """Send thank you letter to all Donors"""
    message = "Dear {:s},\n\
    Thank you for donating ${:,.2f}.\n\
    Sincerely,\n\
    Your Local Charity"
    query = donor.find()
    for item in query:
        with open(item['full_name'] + ".txt",'w') as output:
            output.write(message.format(item['full_name'], item['total_donation']))
    print("Letters have been generated.")


def generate_report():
    """Generates a report of Donor data"""
    donation_total = []
    query = donor.find()
    for item in query:
        donation_total.append(
            [item['full_name'],
            item['total_donation'],
            item['donation_count'],
            item['total_donation']/item['donation_count']])
    donation_total.sort(key=lambda l: l[1], reverse = True)
    s1 = "Donor Name          |   Total Given  |  Num Gifts |  Average Gift\n"
    s2 = "-----------------------------------------------------------------\n"
    final_string = s1 + s2
    for z in range(0, len(donation_total)):
        s3 = '{:20} ${:13,.2f}{:14}  ${:13,.2f}\n'.format(*donation_total[z])
        final_string += s3
    return final_string


def print_report():
    """Print report of Donor data"""
    print(generate_report())


def get_donor_name():
    """Prompts user for Donor name"""
    return input("Enter a full name: ")


def get_new_donor_amount():
    """Prompts user for a donation entry"""
    return input("Enter a donation amount: ")


def clear_db():
    """Clean database for reuse."""
    db.drop_collection('donor')
    print("Database has been cleared. Exiting...")
    quit()


def main_prompt():
    """Prompts the user for option selection"""
    response = input("\n\
        Choose from one of 4 actions:\n\
        1) Add a Donation\n\
        2) Delete a Donor\n\
        3) Update a Donor\n\
        4) Create a Report\n\
        5) Send letters to everyone\n\
        0) Quit\n\
        Please type 1, 2, 3, 4, 5, or 0: ")
    return response


def action(switch_dict):
    """User prompt and interface."""

    while True:
        user_input = main_prompt()
        try:
            switch_dict.get(user_input)()
        except (TypeError, ValueError):
            print("Invalid input, {} please try again.".format(user_input))


# Python program to use main for function call
if __name__ == "__main__":
    with login_database.login_mongodb_cloud() as connect:
        donor_db = donor_data.get_donor_data()
        db = connect['dev']
        donor = db['donor']
        donor.insert_many(donor_db)

        switch_dict = {
            'list': print_names,
            '1': add_donation,
            '2': delete_donor,
            '3': update_donor,
            '4': print_report,
            '5': send_letters,
            '0': clear_db
        }
        action(switch_dict)
