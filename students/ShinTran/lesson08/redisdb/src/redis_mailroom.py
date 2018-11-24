'''
Shin Tran
Python 220
Lesson 8 Assignment
'''

#!/usr/bin/env python3
# Implementing the mailroom program using a database connection


from decimal import Decimal
from pprint import pprint as pp
import logging
import login_database
import redis
import sys
import utilities


log = utilities.configure_logger('default', '../logs/mongodb_script.log')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_name_list():
    """Creates a list of all the distinct donors, returns a list
    helper method for print_names"""
    donor_list  = []
    for item in r.keys():
        donor_list.append(item)
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

'''
def add_donation():
    """Prompts the user to type a name of a donor, enter a donation amount,
    prints an email thanking the donor
    If the user types exit, it would return to the main prompt"""
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
            print(get_email_text(temp_list))


def delete_donor():
    """Prints all the Donor Names, prompts the user to type
    a donation name to delete, removes the Donor from the
    table accordingly"""
    logger.info("Connecting to DB, to delete a Donor record")
    donor_name = get_donor_name()
    if donor_name in generate_name_list():
        del_query = donor.delete_many({'full_name': donor_name})
    logger.info('Database delete successful')



def update_donor():
    """Prompts the user to type a Donor name to update,
    prompts the user to enter a series of donations"""
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
'''

def generate_report():
    """Generates a report of all the previous donators
    Report includes name, total donated, count of donations, average gift
    Report is also formatted with a certain spacing
    returns the report as a string"""
    donation_total = []
    for item in r.keys():
        dn_name = str(item)

        dn_list = list(r.hmget(item, 'donations')[0].split()[1:-1])
        
        total_dn = sum(dn_list)
        dn_count = len(dn_list)

        print("tot " + total_dn)
        print("cnt " + dn_count)

        avg_dn = 100 #total_dn/dn_count

        donation_total.append(
            [dn_name, total_dn, dn_count, avg_dn])
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


def get_donor_name():
    """Prompts the user for a donor name"""
    return input("Enter a full name: ")


def get_new_donor_amount():
    """Prompts the user for a donation amount"""
    return input("Enter a donation amount: ")


def clear_db():
    r.flushdb()
    print("Database has been cleared. Exiting...")
    quit()


def main_prompt():
    """Prompts the user to enter an option"""
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
    try:
        log.info('Step 1: connect to Redis')        
        r = login_database.login_redis_cloud()
        log.info('Step 2: Adding 4 donors to the data cache')
        r.hmset('Bom Trady',
            {'phone': '295-647-7874',
            'zip': 57672,
            'email': 'btrady@email.com',
            'donations': [500.00, 750.00, 1000.00, 1250.00, 1500.00]})
        r.hmset('Raron Aodgers',
            {'phone': '905-306-9770',
            'zip': 74089,
            'email': 'raodgers@email.com',
            'donations': [1500.00, 2000.00]})
        r.hmset('Brew Drees',
            {'phone': '644-113-0350',
            'zip': 44870,
            'email': 'bdrees@email.com',
            'donations': [2000.00, 3500.00, 5000.00]})
        r.hmset('Meyton Panning',
            {'phone': '235-587-5642',
            'zip': 40087,
            'email': 'mpanning@email.com',
            'donations': [1500.00, 8500.00]})
        switch_dict = {
            'list': print_names,
            #'1': add_donation,
            #'2': delete_donor,
            #'3': update_donor,
            '4': print_report,
            #'5': send_letters,
            '0': clear_db
        }
        action(switch_dict)
    except Exception as e:
        print(f'Redis error: {e}')
        