
import pprint
import login_database
import utilities
from pathlib import Path
import os
import pymongo 
from pymongo import MongoClient
import configparser
import pprint
import sys


log = utilities.configure_logger('default', '../logs/mongodb_script.log')
config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


donors = [{'donor': 'Bill Gates',
          'donations': [6000, 456,33]},
          {'donor': 'Jeff Bezos',
           'donations': [10000, 3000]},
          {'donor': 'Hannah Smith',
           'donations': [60000, 7800]},
          {'donor': 'John Clark',
           'donations': [3000, 890]},
          {'donor': 'Andrew Jones',
           'donations': [8000]}]


def read():
    """Print database"""
    try:
        for donation in donations.find():
            pprint.pprint(donation)
    except Exception as e:
      log.info(e)


def add():
    """
        Add a new donor and donation amount to the database
    """
    donor_name = input("Enter the name of a new donor ")
    donation_amount = int(input("Enter new donation amount "))
    try:
        donations.insert_one(
          {'donor': donor_name,
           'donations': [donation_amount]
        })
        print('New donor added succesfully')
        read()
    except Exception as e:
      log.info(e)


def update_donor_name():
    """
         Update name for an existing donor
    """
    name = input('Enter the name of the donor to be updated ')
    new_name = input('Enter new name for this donor ')
    try:
        donations.update_one(
            {"donor": name},
            {"$set": {"donor": new_name}})
    except Exception as e:
        log.info(e)


def update_donation(name, amount):
    """
        Update donation amount for an existing donor
    """
    try:
        donations.update_one(
            {"donor": name},
            {"$push": {"donations": amount}})
    except Exception as e:
        log.info(e)


def delete():
    """
        Delete donor from database
    """
    name = input('Enter the name of the donor to be deleted ')
    try:
        donations.delete_one({"donor": name})
    except Exception as e:
        log.info(e)


def list():
    """
        Print list
    """
    try:
        for donation in donations.find():
            pprint.pprint(donation["donor"])
    except Exception as e:
        log.info(e)


def thank_you_note():
    """Send a thank you note and update the list of donors (updates donation amount for an existing donor)"""
    name = input("Please, type the full name of an existing sponsor from the list: ")
    while name == "list":
        list()
        name = input("Please, type the full name of a sponsor: ")
    while name.isnumeric():
        name = input("Please, type the full name of a sponsor. Your input should be a string: ")
    amount = int(input("How much would you like to donate? "))
    update_donation(name, amount)
    print(f"Dear {name},\n\n\tThank you for your generous donation in the amount of ${amount}.\n\n\t\t\t\t\t\t\tSincerely, your Charity")


def create_report():
    """
        Print report 
    """
    print("{0:<20}{1:>12}{2:>12}{3:>15}".format("Donor Name", "Total Given", "Num Gifts", "Average Gift"))
    print("--------------------------------------------------------------")
    try:
        for donation in donations.find():
            total = sum(donation["donations"])
            num = len(donation["donations"])
            average = total/num
            pprint.pprint("{:<20} ${:>12,.2f}{:^12} ${:>12,.2f}".format(donation["donor"], total, num, average))      
    except Exception as e:
        log.info(e)


def letter_to_all():
    """
       print letter to all donors and save each letter do a disk
    """
    try:
        for donation in donations.find():
          name = donation["donor"]
          directory = str(input("Please specify the directory name for this file: "))
          filepath = os.path.join(os.sep, directory)
          with open(f"{filepath}\\{name}.txt", "w") as f:
                f.write("Dear {0},\n\n\tThank you for your very kind donation. It will be put to very good use.\n\n\t\t\t Sincerely,\n\t\t\t -The Team".format(name))
    except Exception as e:
        logger.info(e)

 
def quit():
    """exit the running program"""
    db.drop_collection('donations')
    sys.exit()


dict_select = {
1: thank_you_note,
2: create_report,
3: letter_to_all,
4: update_donor_name,
5: add,
6: delete,
7: quit
}
    

if __name__ == '__main__':
    with login_database.login_mongodb_cloud() as client:
        db = client['mailroom'] 
        donations = db['donations']
        results = donations.insert_many(donors)
        while True:
            action = int(input(("Please tell us what you would like to do: 'send a thank you: type 1',"
                            " 'create a report: type 2', 'send a letter to all donors: type 3', update a donor name: type 4'"
                          "'add a new donor: type 5', 'delete a donor record: type 6', 'quit: type 7' ")))
            dict_select[action]()
    



