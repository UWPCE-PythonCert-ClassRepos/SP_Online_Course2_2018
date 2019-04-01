#!/usr/bin/env python3

# Lesson_8 Activity 2 NOSQL mailroom

import os
import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth
import login_database
import utilities
import pprint

log = utilities.configure_logger('default', '../mailroom_nosql.log')
    
    
def get_donor_list():
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        donor_names = session.run("match (n:Person) return n.full_name")
    return [d[0] for d in donor_names]


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
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        donor_list = session.run("match (n:Person) return n.full_name, n.donation")
        print(donor_list)
        for d in donor_list:
            report_list.append([d[0], sum(d[1]), len(d[1])])
    page_break()
    col_lab = ["Donor Name", "Total Given", "Num Gifts", "Average Gift"]
    max_name = max([len(j[0]) for j in report_list])
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
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        if name not in get_donor_list():
            addname = input("The name you selected is not in the list,"
                            " would you like to add it(y/n)? ")
            if addname[0].lower() == 'y':
                amount = get_amount()
                session.run("create (n:Person {full_name: '%s', donation: [%02.2f]})" % (name, amount))
            elif addname.lower() == 'exit':
                return
            else:
                print("\nName was not added, try again\n")
                return
        else:
            log.info(f'Donor {name} found in database')
            amount = get_amount()
            donor_names = session.run("MATCH (n:Person) return n.full_name, n.donation")
            for d in donor_names:
                if name == d[0]:
                    d[1].append(amount)
                    session.run("MATCH (n:Person { full_name: '%s' }) SET n.donation = %a" % (name, d[1]))        

  

def delete_donor():
    """remove a donor from the database"""
    delete_name = input("Whose donations are we removing from the database? \n")
    if delete_name in get_donor_list():
        with driver.session() as session:
            name = "match (n:Person {full_name: '%s'}) delete n" % (delete_name)
            session.run(name)
            print(f'{name} was deleted from the database.')
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
