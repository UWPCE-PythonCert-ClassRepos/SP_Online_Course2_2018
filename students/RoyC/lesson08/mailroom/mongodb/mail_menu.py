#!/usr/bin/env python3
# Lesson 9, mailroom menu

import logging
import configparser
import pymongo

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
                print("Amt: {:.2f}".format(donation['amount']))
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
            
def init_db(db):
    """
    Initialize the database
    """
    donor_data = [
        {
            'name': 'Ned Flanders',
            'total_donations': 2050.60,
            'average_donation': 1025.30
        },
        {
            'name': 'Martin Prince',
            'total_donations': 31.78,
            'average_donation': 15.89
        },
        {
            'name': 'Edna Krabappel',
            'total_donations': 249.33,
            'average_donation': 83.11
        },
        {
            'name': 'Homer Simpson',
            'total_donations': 1126.13,
            'average_donation': 375.37666
        },
        {
            'name': 'Moe Szylak',
            'total_donations': 54.23,
            'average_donation': 54.23
        }
    ]
    donation_data = [
        {
            'name': 'Ned Flanders',
            'amount': 1200.25
        },
        {
            'name': 'Ned Flanders',
            'amount': 850.35
        },
        {
            'name': 'Martin Prince',
            'amount': 12.22
        },
        {
            'name': 'Martin Prince',
            'amount': 19.56
        },
        {
            'name': 'Edna Krabappel',
            'amount': 55.43
        },
        {
            'name': 'Edna Krabappel',
            'amount': 118.67
        },
        {
            'name': 'Edna Krabappel',
            'amount': 75.23
        },
        {
            'name': 'Homer Simpson',
            'amount': 253.64
        },
        {
            'name': 'Homer Simpson',
            'amount': 772.50
        },
        {
            'name': 'Homer Simpson',
            'amount': 99.99
        },
        {
            'name': 'Moe Szylak',
            'amount': 54.23
        }
    ]
    donors = db['donors']
    donors.insert_many(donor_data)
    donation_records = db['donation_records']
    donation_records.insert_many(donation_data)

config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()
    
def login_mongodb():
    """
    Connect to the mongo db cloud
    """
    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]

    except Exception as e:
        print(f'error: {e}')

    client = pymongo.MongoClient(f'mongodb://{user}:{pw}'
                                 '@cluster0-shard-00-00-vxcnj.mongodb.net:27017,'
                                 'cluster0-shard-00-01-vxcnj.mongodb.net:27017,'
                                 'cluster0-shard-00-02-vxcnj.mongodb.net:27017/test'
                                 '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')
    return client

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

    # login to mongodb
    client = login_mongodb()
    db = client['mailroom']
    
    # initialize collections if they don't exist
    collist = db.list_collection_names()
    if not "donors" in collist:
        init_db(db)
    
    # create a donor records set
    donation_records = DonationRecords(db)

    display_menu(main_prompt, main_menu, donation_records)
