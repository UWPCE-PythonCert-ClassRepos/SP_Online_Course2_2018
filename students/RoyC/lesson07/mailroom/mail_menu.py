#!/usr/bin/env python3
# Lesson 9, mailroom menu

import logging

from peewee import *
from mailroom import Donor, DonationRecords

# create a donor records set
donation_records = DonationRecords()

def record_donation():
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
            
def update_donation():
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
                print("Amt: {:.2f}".format(donation.amount))
            old_amt = input("Enter donation to update: ")
            new_amt = input("Enter new donation amout: ")
            donor.update_donation(old_amt, new_amt)
            break
        print("Donor not found")
    
def print_report():
    """
    Print the donor report to the screen
    """
    print(donation_records.create_report())
            
def thank_all():
    """
    Write thank you letters for all donors to separate files
    """
    donation_records.thank_all()
    
def clear_donor_list():
    """
    Clear the donor list
    """
    confirm = input("\n\nYou are about to clear all donor records! Are you sure? (Enter YES):")
    if confirm == "YES":
        # create a new DonationRecords object to clear
        donation_records.clear_donations()
        print("\nDonor records have been cleared\n")
        
def quit_menu():
    """
    Return text to indicate operator selects quit
    """
    return "quit selected"

def display_menu(prompt, menu_dict):
    """
    Continually display the given options prompt, then prompt for a selection and invoke
    associated function from menu dict. If function returns exit string, then break loop.
    """
    while True:
        choice = input(prompt)
        try:
            if menu_dict[choice]() == "quit selected":
                break;
        except KeyError:
            print("\nThat is not one of the choices!\n")
            
def init_db():
    """
    Initialize the database
    """
    

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

    # open the database
    try:
        database = SqliteDatabase('mailroom.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
    except Exception as e:
        logger.error("Error initializing dabase", e)

    display_menu(main_prompt, main_menu)
    
    # close the database
    try:
        database.close()
    except Exception as e:
        logger.error("Unable to close database", e)
 

