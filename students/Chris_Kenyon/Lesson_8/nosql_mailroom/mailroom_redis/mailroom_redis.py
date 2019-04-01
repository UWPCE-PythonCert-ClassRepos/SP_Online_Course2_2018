#!/usr/bin/env python3

# Lesson_8 Activity 2 NOSQL mailroom

import os
import configparser
from pathlib import Path
import redis
import login_database
import utilities
import pprint

log = utilities.configure_logger('default', '../mailroom_nosql.log')
    
    
def get_donor_list():
    log.info('Retrieving donor list')
    r = login_database.login_redis_cloud()
    all_donors = []
    rcrds = r.keys()
    return rcrds


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
    report = []
    report_list = []
    r = login_database.login_redis_cloud()
    donor_list = get_donor_list()
    for donor in donor_list:
        donations = ''.join(r.hmget(donor, 'Donation'))
        report_list.append([donor, sum(float(i) for i in donations.split(', ')), len(donations.split())])
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


def print_report(donors_obj=None):
    print(create_report())


def add_donation(name):
    """ add a donation for a new or existing donor """
    r = login_database.login_redis_cloud()
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
    log.info(f'Donor {name} found in database')
    amount = get_amount()
    donations = r.hmget(name, 'Donation')
    if donations == ['']:
        donations = str(amount)
    else:
        donations.append(amount)
        donations = ', '.join(str(s) for s in donations)
    r.hmset(name, {'Donation': donations})
    
        


def add_donor(name):
    r = login_database.login_redis_cloud()
    if name not in get_donor_list():
        r.hmset(name, {'Donation': '', 'Email': f'{name}@email.com'})
        print(f"Added {name} to the database")


def delete_donor():
    """remove a donor from the database"""
    delete_name = input("Whose donations are we removing from the database? \n")
    r = login_database.login_redis_cloud()
    if delete_name in get_donor_list():
        r.delete(delete_name)
        log.info(f'{delete_name} has been deleted')
    else:
        print("Can't find the name you want to delete.")

def find_email():
    name = input("Type a donor's name to find their email: \n -->")

    print(r.hget(name, 'Email'))


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
