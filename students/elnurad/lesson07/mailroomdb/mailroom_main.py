#!/usr/bin/python
import os
import os.path
from mailroom_db import *
import logging 

 #donor_models.
        
class DonorCollection(): #DonorCollection = DonorCollection(database)
    """create a class that represents a collection of donors"""
    def __init__(self, database):
        self.database = database

    #working OKAY
    def is__in_list(self, donor):#query = Facility.select().where(Facility.name.contains('tennis'))

        """Check whether donor already exists in the list of donors."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                if Donor.select().where(Donor.donor_name.contains(donor)):
                    return True
                        
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()

        

   
    def add_donation_to_list(self, name, amount):
        """Add a new donation amount to an existing donor's name."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                for donation in Donation.select():
                    if donation.donor_name == name:
                        donation.donation_amount.append(amount)
                        print(f"Dear {name},\n\n\tThank you for your generous donation in the amount of ${amount}.\n\n\t\t\t\t\t\t\tSincerely, your Charity")
                        donation.save()
                logger.info('Donation updated succesfully')
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()



    def add_new_donor(self, name, amount):
        """Add a new donor name and donation amount."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                new_donation = Donation.insert(
                    donation_amount = amount,
                    donor_name = name
                    ).execute()
                new_donor = Donor.insert(
                    donor_name = name,


                    ).execute()                 
                # new_donation.save()
                logger.info('new donation added')
                print(f"Dear {name},\n\n\tThank you for your generous donation in the amount of ${amount}.\n\n\t\t\t\t\t\t\tSincerely, your Charity")
        
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()


    #working OKAY
    def list(self):
        """print a list of donors"""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                for donor in Donor.select():
                    print(donor.donor_name)
        
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()



    def create_report(self):
        """create a formatted report with donor statistics"""
        print("{0:<20}{1:>12}{2:>12}{3:>15}".format("Donor Name", "Total Given", "Num Gifts", "Average Gift"))
        print("--------------------------------------------------------------")
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                for donor in Donor.select():
                    print("{:<20} ${:>12,.2f}{:^12} ${:>12,.2f}".format(donor.donor_name, donor.total_donations,
                                                                       donor.donation_number, donor.average_donation))
        except Exception as e:
            logger.info(e)
        finally:
            self.database.close()


def thank_you_note():
    """Send a thank you note and update the list of donors"""
    name = input("Please, type the full name of a sponsor: ")
    while name == "list":
        donors.list()
        name = input("Please, type the full name of a sponsor: ")
    while name.isnumeric():
        name = input("Please, type the full name of a sponsor. Your input should be a string: ")
    amount = int(input("How much would you like to donate? "))
    if donors.is__in_list(name):
        donors.add_donation_to_list(name, amount)
    else:
        donors.add_new_donor(name, amount)


def quit():
    """exit the running program"""
    exit()
  


database = SqliteDatabase('mailroom.db')
donors = DonorCollection(database)


print(donors.is__in_list('Elnura'))

# dict_select = {
# 1: thank_you_note,
# 2: donors.create_report,
# 3: quit
# }


# if __name__ == '__main__':
#     while True:
#         action = int(input(("Please tell us what you would like to do: 'send a thank you: type 1', 'create a report: type 2', 'quit: type 4' ")))
#         dict_select[action]()
    


