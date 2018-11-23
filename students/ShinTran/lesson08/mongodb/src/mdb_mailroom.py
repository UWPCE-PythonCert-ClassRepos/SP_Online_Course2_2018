'''
Shin Tran
Python 220
Lesson 8 Assignment
'''

#!/usr/bin/env python3
# Implementing the mailroom program using a database connection


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
    """Creates a list of all the distinct donors, returns a list
    helper method for print_names"""
    donor_list  = []
    results = donor.find()
    for item in results:
        donor_list.append(item['full_name'])
    return list(donor_list)


def print_names():
    """Prints out all the names in the name list,
    references generate_name_list"""
    for name in generate_name_list():
        print(name)


def get_email_text(current_donation):
    """Prints a thank you email to a donator
    Donor name and amount is passed in as a parameter"""
    return "Dear {:s},\n\
        Thank you for the generous donation of ${:,.2f}.\n\
        Sincerely,\n\
        Your Local Charity".format(*current_donation)


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
            logger.info("Connecting to DB, to add to the Donor records")
            if donor_name in generate_name_list():
                for item in donor.find():
                    if item['full_name'] == donor_name:
                        current_values = {
                            'full_name': item['full_name'],
                            'donation_count': item['donation_count'],
                            'total_donation': item['total_donation'],
                            'donations': item['donations']
                        }
                        dn_list = item['donations']
                        dn_list.append(temp_list[1])
                        new_values = {
                            'full_name': item['full_name'],
                            'donation_count': item['donation_count'] + 1,
                            'total_donation': item['total_donation'] + temp_list[1],
                            'donations': dn_list
                        }
                        # Line not working
                        donor.update_one(current_values, {'$set': new_values})
                        print("Database has been updated.")
                # For debugging
                for item2 in donor.find():
                    pp(item2)
            else:
                new_donor = {
                    'full_name': temp_list[0],
                    'donation_count': 1,
                    'total_donation': temp_list[1],
                    'donations': [temp_list[1]]
                }
                donor.insert_one(new_donor)
            logger.info('Database add successful')
            print(get_email_text(temp_list))

'''
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
'''

def print_donations():
    """Connects to the database Donations table,
    prints out every record"""
    query = donor.find()
    pp("Donor Name           | Donation")
    pp("---------------------------------------")
    for item in query:
        pp("{:20} | {:8}".format(str(item['full_name']), item['donation']))
    print()


def send_letters():
    """Goes through all the previous donators, gets their total donated,
    sends a thank you letter that is output on a .txt file"""
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
    """Generates a report of all the previous donators
    Report includes name, total donated, count of donations, average gift
    Report is also formatted with a certain spacing
    returns the report as a string"""
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
    """Prints a report of all the previous donators references generate_report"""
    print(generate_report())

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


def clear_db():
    db.drop_collection('donor')
    print("Database has been cleared. Exiting...")
    quit()


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


# Python program to use main for function call
if __name__ == "__main__":
    with login_database.login_mongodb_cloud() as client:
        donor_db = donor_data.get_donor_data()
        db = client['dev']
        donor = db['donor']
        donor.insert_many(donor_db)

        switch_dict = {
            'list': print_names,
            '1': add_donation,
            #'2': delete_donation,
            #'3': update_donation,
            '4': print_report,
            '5': send_letters,
            '0': clear_db
        }
        action(switch_dict)
        