#!/usr/bin/env python3

# Lesson_8 Activity 2 NOSQL mailroom

import os
import configparser
from pathlib import Path
import pymongo
import login_database
import utilities
import pprint

log = utilities.configure_logger('default', '../mailroom_nosql.log')
    
    
def get_donor_list():
    log.info('Listing all donors')
    with login_database.login_mongodb_cloud() as client:
        db = client['donor_chart']
        mailroom = db['mailroom']
        rcrd = mailroom.find()
        all_donors = []
        for item in rcrd:
            all_donors.append(item['donor_name'])
        return all_donors


def page_break():
    """ Print a separator to distinguish new 'pages'"""
    print("_"*75+"\n")


def get_amount():
    """Get valid donation amount from user"""
    while True:
        try:
            amount = input("How much did they donate: ")
            if str(amount).lower() == 'exit':
                return amount
            else:
                return float(amount)
        except ValueError:
            print("you have made an invalid choice, try again.")


def menu_page(option=None):
    """ Return valid menu option from user """
    while True:
        try:
            print("Please choose one of the following options(1,2,3,4):"
                  "\n1. Send a Thank you. \n2. Create a report"
                  "\n3. Delete a donation \n4. Quit")
            option = int(input('--->'))
        except ValueError:
            print("You have made an invalid choice, try again.")
            page_break()
            continue
        return option


def send_thanks():
    """ Send Thanks """
    page_break()
    while True:
        print("To whom would you like to say thank you?\n"
              "(type \"list\" for a full list of names or"
              "\"exit\" to return to the menu)")
        name = input("--->")
        if name == 'list':
            print(("{}\n"*len(get_donor_list())).format(*get_donor_list()))
            continue
        add_donation(name)
        break


def create_report():
    """ Create Report """
    with login_database.login_mongodb_cloud() as client:
        db = client['donor_chart']
        mailroom = db['mailroom']    
        report = []
        report_list = []
        donor_list = get_donor_list()
        for donor in donor_list:
            rcrd = mailroom.find_one(
                {
                    'donor_name': donor
                }
            )
            report_list.append([donor, sum(rcrd['donations']), len(rcrd['donations'])])
    page_break()
    col_lab = ["Donor Name", "Total Given", "Num Gifts", "Average Gift"]
    max_name = max([len(donor) for donor in donor_list])
    max_don = max([item[1] for item in report_list])
    float_max = (f"{(max_don):,.2f}")
    max_donl = len(str(float_max))
    max_gift = len(col_lab[2])
    if max_donl < len(col_lab[1]):
        max_donl = len(col_lab[1])
    format_col = "\n{:<" + "{}".format(max_name+5) + "}|{:^"
    format_col += "{}".format(max_donl+5)
    format_col += "}|{:^" + "{}".format(max_gift+5)
    format_col += "}|{:>" + "{}".format(max_donl+5) + "}"
    print(format_col.format(*col_lab))
    print("-"*len(format_col.format(*col_lab)))

    sorted_list = sorted(report_list, key=lambda kv: kv[1], reverse=True)
    for name in sorted_list:
        num_gifts = name[2]
        avg_gift = name[1]/name[2]
        format_item = "{:<" + "{}".format(max_name+5) + "}${:>"
        format_item += "{}".format(max_donl+5) + ",.2f}{:>"
        format_item += "{}".format(max_gift+5) + "d} ${:>"
        format_item += "{}".format(max_donl+5) + ",.2f}"
        report.append(format_item.format(name[0], name[1],
                                         num_gifts, avg_gift))
    report.append(f"Total raised = $ {sum(name[1] for name in sorted_list):,.2f} "
                  f"from {sum(name[2] for name in sorted_list)} donations")
    return '\n'.join(report)


def total_key(donor):
    """ Return total donation key for sorting function """
    return(donor.donation_total)


def print_report(donors_obj=None):
    print(create_report())


def add_donation(name):
    """ add a donation for a new or existing donor """
    log.info('Searching for donor')
    if name not in get_donor_list():
        addname = input("The name you selected is not in the list,"
                        " would you like to add it(y/n)? ")
        if addname[0].lower() == 'y':
            add_donor(name)
        elif addname.lower() == 'exit':
            return
        else:
            print("\nName was not added, try again\n")
            return
    with login_database.login_mongodb_cloud() as client:
        db = client['donor_chart']
        mailroom = db['mailroom']
        rcrd = mailroom.find_one(
            {
                'donor_name': name
            }
        )
        log.info(f'Donor {name} found in database')
        amount = get_amount()
        all_donations = rcrd['donations']
        log.info('Donations: {}'.format(all_donations))
        all_donations.append(amount)
        log.info('New Donations: {}'.format(all_donations))
        log.info('New record: {}'.format(rcrd))
        mailroom.find_one_and_update(
            {"_id": rcrd["_id"]},
            {'$set': {"donations": rcrd["donations"]}}
        )
        log.info('Check if the record was updated')
        new_rcrd = mailroom.find_one(
            {
                'donor_name': name
            }
        )
        log.info('New record from DB: {}'.format(new_rcrd))


def add_donor(name):
    log.info(f'Added {name} as a new donor')
    with login_database.login_mongodb_cloud() as client:
        db = client['donor_chart']
        mailroom = db['mailroom']
        mailroom.insert(
            {
                'donor_name': name,
                'donations': []
            }
        )
        log.info('Check if {} was added: {}'.format(
            name,
            mailroom.find_one(
                {
                    'donor_name': name
                })))



def delete_donor():
    """remove a donor from the database"""
    delete_name = input("Whose donations are we removing from the database? \n")

    if delete_name in get_donor_list():
        with login_database.login_mongodb_cloud() as client:
            db = client['donor_chart']
            mailroom = db['mailroom']        
            mailroom.delete_one( 
                {
                    'donor_name': delete_name                   
                }
            )
        print(f'{delete_name} has been removed from the database.')
    else:
        print("Can't find the name you want to delete.")


def menu_quit():
    """ return quit for menus """
    return "Quit"


options = range(1, 5)
test_dump = "C:/Users/chris.kenyon/Documents/Kenyon/UWPython/Testing_File_dump"
menus = (send_thanks, print_report, delete_donor, menu_quit)
menu_dict = dict(zip(options, menus))

if __name__ == '__main__':
    option = 0
    while True:
        page_break()
        try:
            option = menu_page()
            #if option == 3:
                #menu_dict[option](test_dump)
            if menu_dict[option]() == "Quit":
                break
        except KeyError:
            print("You have made an invalid choice, try again.")
            page_break()
