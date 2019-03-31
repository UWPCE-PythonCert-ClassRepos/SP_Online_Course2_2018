#!/usr/bin/env python3
# Lesson 9, mailroom menu

import logging
import configparser

from neo4j.v1 import GraphDatabase, basic_auth
from pathlib import Path
from mailroom import Donor, DonationRecords

def record_donation(donation_records):
    """
    Prompt operator for donor name, or 'list' to see names of donors on record.
    Take name entered and either use existing donor, or add new record.
    Then prompt for amount of this donation, then save the donation record
    and print a thank you note.
    """
    while True:
        donor_name = input("\nEnter full name of donor (or 'list' to see names of donors): ")
        if donor_name == "list":
            for d in donation_records.donors:
                print(d.name)
            print()
        else:
            amt = 0.0
            while True:
                try:
                    amt = float(input("Enter amount of donation: "))
                except ValueError:
                    print("Not a valid donation format, please enter a number")
                else:
                    break
            donor = donation_records.record_donation(donor_name, amt)
            print(donation_records.send_thanx(donor, amt))
            break
            
def update_donation(donation_records):
    """
    Update an existing donation
    """
    # print out name of donors
    for d in donation_records.donors:
        print(d.name)
    # prompt for donor to update
    while True:
        donor_name = input("\nEnter full name of donor to update (or q to quit): ")
        if donor_name == "q":
            break
        donor = donation_records.get_donor(donor_name)
        if donor != None:
            for donation in donor.donations:
                print("Amt: {}".format(donation))
            old_amt = input("Enter donation to update: ")
            new_amt = input("Enter new donation amout: ")
            donor.update_donation(old_amt, new_amt)
            break
        print("Donor not found")
    
def print_report(donation_records):
    """
    Print the donor report to the screen
    """
    print(donation_records.create_report())
            
def thank_all(donation_records):
    """
    Write thank you letters for all donors to separate files
    """
    donation_records.thank_all()
    
def clear_donor_list(donation_records):
    """
    Clear the donor list
    """
    confirm = input("\n\nYou are about to clear all donor records! Are you sure? (Enter YES):")
    if confirm == "YES":
        # create a new DonationRecords object to clear
        donation_records.clear_donations()
        print("\nDonor records have been cleared\n")
        
def quit_menu(donation_records):
    """
    Return text to indicate operator selects quit
    """
    return "quit selected"

def display_menu(prompt, menu_dict, donation_records):
    """
    Continually display the given options prompt, then prompt for a selection and invoke
    associated function from menu dict. If function returns exit string, then break loop.
    """
    while True:
        choice = input(prompt)
        try:
            if menu_dict[choice](donation_records) == "quit selected":
                break;
        except KeyError:
            print("\nThat is not one of the choices!\n")
            
def init_db(driver):
    """
    Initialize the database
    """
    with driver.session() as session:
        # clear the data
        cyph = "MATCH (n) DETACH DELETE n"
        session.run(cyph)
        # initialize with new data
        for name, donations in [('Ned Flanders', [1200.25, 850.35]),
                                ('Martin Prince', [12.22, 19.56]),
                                ('Edna Krabappel', [55.43, 118.67, 75.23]),
                                ('Homer Simpson', [253.64, 772.50, 99.99]),
                                ('Moe Szylak', [54.23])
                               ]:
            total = 0.0
            avg = 0.0
            for amt in donations:
                total += float(amt)
            if len(donations) > 0:
                avg = total / float(len(donations))
            cyph = "CREATE (n:Donor {name:'%s', total_donations: %f, average_donation: %f}) RETURN id(n)" % (name, total, avg)
            result = session.run(cyph)
            donor_id = result.single()[0]
            for donation in donations:
                cyph = "CREATE (n:Donation {amount:%s}) RETURN id(n)" % (donation)
                result = session.run(cyph)
                donation_id = result.single()[0]
                cyph = "MATCH (d:Donation),(d1:Donor) WHERE ID(d) = %s and ID(d1) = %s CREATE (d)-[donated:DONATED]->(d1) RETURN d, d1" % (donation_id, donor_id)
                session.run(cyph)


config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()
    
def login_neo4j():
    """
    Connect to the neo4j cloud
    """
    config.read(config_file)
    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-opmhmhgpkdehgbkejbochpal.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))
    return driver

# main menu prompt text
main_prompt = ("\nPlease choose one of these options:"
               "\n   1 - Record Donation"
               "\n   2 - Update Record"
               "\n   3 - Create a Report"
               "\n   4 - Send letters to Everyone"
               "\n   5 - Clear donor data"
               "\n   q - Quit"
               "\nEnter your selection => "
            )

# main menu dictionary, options and associated functions            
main_menu = {"1": record_donation,
             "2": update_donation,
             "3": print_report,
             "4": thank_all,
             "5": clear_donor_list,
             "q": quit_menu
            }
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    logger = logging.getLogger(__name__)

    # login to neo4j
    driver = login_neo4j()
    
    init_db(driver)
    
    # create a donor records set
    donation_records = DonationRecords(driver)

    display_menu(main_prompt, main_menu, donation_records)
