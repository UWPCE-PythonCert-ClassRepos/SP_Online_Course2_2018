#!/usr/bin/python
import os
import os.path
from mailroom_db import *
from populate_db import *
import logging 

 

def add_donor():
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    name = input('Please, type the full name of a new donor ')
    amount = int(input('Please, type the new donation amount '))
    try:    
        new_donor = Donor.create(
                    donor_name = name)
        new_donor.save()
        logger.info('Database add successful: {}')
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

# def calculate_records(name):
#     database = SqliteDatabase('mailroom.db')
#     database.connect()
#     database.execute_sql('PRAGMA foreign_keys = ON;')

    #need to select a donor
    #calculate avg_don, num_don, total_don
    #total_don = 0, with each iteration over donations +=1
    #num_don = 0, with each iteration over dontaion += 1
    #ave_don = total_don/num_don




def create_report():

    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    # print("{0:<20}{1:>12}{2:>12}{3:>15}".format("Donor Name", "Total Given", "Num Gifts", "Average Gift"))
    # print("--------------------------------------------------------------")
    try:
        query = (Donor
                 .select(Donor, Donation)
                 .join(Donation, JOIN.INNER)
                 )
        logger.info('Printing matching records')
        for donor in query:
            logger.info(f'{donor.donor_name}, {donor.donation.donation_amount}')
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closed')
        database.close()


# print("{:<20} ${:>12,.2f}{:^12} ${:>12,.2f}".format(member.name, member.total_donations, member.donations_number, member.average_donation))
# donor.donor_name
# donor.donation.donation_amount




# add_donor()
create_report()





# def add_donation():

#     database = SqliteDatabase('mailroom.db')
#     database.connect()
#     database.execute_sql('PRAGMA foreign_keys = ON;')
#     amount = input('Please, type the new donation amount ')
#     try:
#         Donation.create(donor_name)




 #add_donor - if donor doesn't exist
 #if donor exists - add donation


# def add_donation_to_list(self, name, amount):
#         """Add a new donation amount to an existing donor's name."""
#     for member in self.collection:
#         if name == member.name:
#             member.add_donation(amount)
#             print(f"Dear {member.name},\n\n\tThank you for your generous donation in the amount of ${amount}.\n\n\t\t\t\t\t\t\tSincerely, your Charity")
      

# def add_new_donor(self, name, amount):
#     """Add a new donor name and donation amount."""
#     self.collection.append(Donor(name, [amount]))
#     print(f"Dear {name},\n\n\tThank you for your generous donation in the amount of ${amount}.\n\n\t\t\t\t\t\t\tSincerely, your Charity")
    

# def list(self):
#     """print a list of donors"""
#     for member in self.collection:
#         print(f"{member.name}")


# def create_report(self):
#     """create a formatted report with donor statistics"""
#     print("{0:<20}{1:>12}{2:>12}{3:>15}".format("Donor Name", "Total Given", "Num Gifts", "Average Gift"))
#     print("--------------------------------------------------------------")
#     for member in sorted(self.collection, reverse = True):
#         print("{:<20} ${:>12,.2f}{:^12} ${:>12,.2f}".format(member.name, member.total_donations, member.donations_number, member.average_donation))


# def thank_you_note():
#     """Send a thank you note and update the list of donors"""
#     name = input("Please, type the full name of a sponsor: ")
#     while name == "list":
#         donors.list()
#         name = input("Please, type the full name of a sponsor: ")
#     while name.isnumeric():
#         name = input("Please, type the full name of a sponsor. Your input should be a string: ")
#     amount = int(input("How much would you like to donate? "))
#     if donors.is__in_list(name):
#         donors.add_donation_to_list(name, amount)
#     else:
#         donors.add_new_donor(name, amount)
    

# def letter_to_all():
#     """Write a thank you note to each donor and save it to a disk"""
#     for donor in donors.collection:
#         # print(donor)
#         directory = str(input("Please specify the directory name for this file: "))
#         filepath = os.path.join(os.sep, directory)
#         total_don = donor.total_donations
#         with open(f"{filepath}\\{donor.name}.txt", "w") as f:
#             f.write("Dear {0},\n\n\tThank you for your very kind donation of ${1}.\n\n\t\t It will be put to very good use.\n\n\t\t\t Sincerely,\n\t\t\t -The Team".format(donor.name, total_don)) 
     

# def quit():
#     """exit the running program"""
#     exit()
  

# dict_select = {
# 1: thank_you_note,
# 2: donors.create_report,
# 3: letter_to_all,
# 4: quit
# }


# if __name__ == '__main__':
#     while True:
#         action = int(input(("Please tell us what you would like to do: 'send a thank you: type 1', 'create a report: type 2', 'send a letter to all donors: type 3', 'quit: type 4' ")))
#         dict_select[action]()
    

