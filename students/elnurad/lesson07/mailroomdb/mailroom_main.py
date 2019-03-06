#!/usr/bin/python
import os
import os.path
from mailroom_db import *
from populate_db import *
import logging 


def add_donor(name, amount):
    """
       add new donor or update donation history of 
       existing donor
    """
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    try:    
        new_donor = Donor.create(
                    donor_name = name)
        new_donor.save()
        logger.info(f'Database add successful: {new_donor}')
        new_donation = Donation.create(donor_name = new_donor,
                                        donation_amount = amount)
        new_donation.save()
        logger.info('Print the Donor records we saved...')
        
    except IntegrityError:
        logger.info('This donor already exists')
        donor_record = Donor.get(Donor.donor_name == name) #got the existing donor
        new_donation = Donation.create(donor_name = donor_record,
                                       donation_amount = amount)
        new_donation.save()  
        logger.info(f'saved {amount} for {donor_record}')

    finally:
        logger.info('database closes')
        database.close()


def list():
    """
       print list of all donors
    """
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    try:
        query = Donor.select()
        for donor in query:
            print(donor.donor_name)
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closed')
        database.close()


def update_donor():
    """
       update donor name of an existing donor.
    """
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    name = input('Please, type the full name of the donor that needs to be updated ')
    new_name = input('Please type the new name for this donor ')
    try:
        query = (Donor
                 .select(Donor, Donation)
                 .join(Donation, JOIN.INNER))
        for donor in query:
            if donor.donor_name == name:
                donor.donor_name = new_name
                donor.save()      
         
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closed')
        database.close()


def delete_donor():
    """
       delete donor
    """
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    name = input('Please, type the full name of the donor to delete ')
    try:
        query = (Donor
                 .select(Donor, Donation)
                 .join(Donation, JOIN.INNER))
        for donor in query:
            if donor.donor_name == name:
                to_delete = donor.delete_instance()
                donation_delete = donor.donation.delete_instance()
        logger.info(f'deleted {donor} from Donor table')
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closed')
        database.close()


def create_report():
    """
       create report 
    """
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    try:
        query = (Donor
                .select(Donor, Donation)
                .join(Donation, JOIN.INNER))
        report = []
        donors = []
        for donor in Donor.select():
            donors.append(donor.donor_name)
        
        for donor in donors:
            donor_stat = []
            for row in query:
                if row.donor_name == donor:
                    donor_stat.append(row.donation.donation_amount)
            report.append([donor, int(sum(donor_stat)), int(len(donor_stat))])
            report = sorted(report, key = lambda x: x[1], reverse = True)
        
        print("{0:<20}{1:>12}{2:>12}{3:>15}".format("Donor Name", "Total Given", "Num Gifts", "Average Gift"))
        print("--------------------------------------------------------------")
        for person in report:
            print("{:<20} ${:>12,.2f}{:^12} ${:>12,.2f}".format(person[0], person[1], person[2], person[1]/person[2]))      

    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closed')
        database.close()


def letter_to_all():
    """
       print letter to all donors and save each letter do a disk
    """
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    try:
        query = Donor.select()
        for donor in query:
            directory = str(input("Please specify the directory name for this file: "))
            filepath = os.path.join(os.sep, directory)
            with open(f"{filepath}\\{donor.donor_name}.txt", "w") as f:
                f.write("Dear {0},\n\n\tThank you for your very kind donation. It will be put to very good use.\n\n\t\t\t Sincerely,\n\t\t\t -The Team".format(donor.donor_name)) 
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closed')
        database.close()


def thank_you_note():
    """Send a thank you note and update the list of donors"""
    name = input("Please, type the full name of a sponsor: ")
    while name == "list":
        list()
        name = input("Please, type the full name of a sponsor: ")
    while name.isnumeric():
        name = input("Please, type the full name of a sponsor. Your input should be a string: ")
    amount = int(input("How much would you like to donate? "))
    add_donor(name, amount)
    print(f"Dear {name},\n\n\tThank you for your generous donation in the amount of ${amount}.\n\n\t\t\t\t\t\t\tSincerely, your Charity")


def quit():
    """exit the running program"""
    exit()

dict_select = {
1: thank_you_note,
2: create_report,
3: letter_to_all,
4: update_donor,
5: delete_donor,
6: quit
}




if __name__ == '__main__':
    while True:
        action = int(input(("Please tell us what you would like to do: 'send a thank you: type 1',"
                            " 'create a report: type 2', 'send a letter to all donors: type 3', update a donor record: type 4'"
                            "'delete a donor record: type 5', 'to quit: type 6' ")))
        dict_select[action]()
    

