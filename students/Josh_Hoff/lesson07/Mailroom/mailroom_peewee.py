"""
    Mailroom utilizing a database
"""
import sys
import logging
from create_mailroom import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DonorCollection:
    def __init__(self):
        pass
        
    def show_list(self):
        for saved_donor in Donor:
            print(f'{saved_donor}')
        return
            
    def save(self):
        pass

    def load(self):
        pass
        
    def report(self):
        donorq = (Donor.select().order_by(Donor.donor_name)).prefetch(Donation)
        for i in donorq:
            print(i.donor_name)
            for x in i.name_person:
                print(f'  Invoice: {x.dono_number} : ${x.dono}')
            print(f'  Total Donations: ${i.donations}')
            for x in i.person_name:
                print(f'   Transactions - {x.transactions}')
                print(f'   Average Donation - ${x.average}')
                print(f'   First Donation - ${x.first_gift}')
                print(f'   Latest Donation - ${x.last_gift}')
        
    def letters(self):
        pass
    
def show_donations():
    a.show_list()
    while True:
        choice = input(f'Whose donations do you want to see?: ')
        if choice == 'quit':
            return
        for saved_donor in Donor:
            if choice == saved_donor.donor_name:
                print(f'\n{choice}')
                query = (Donation.select().where(Donation.held_by == choice).order_by(Donation.dono_number))
                for ind in query:
                    print(f'Invoice: {ind.dono_number} : ${ind.dono}')
                return
        print('\nDonator does not exist.\n')
        continue
        
def delete():
    new_dict = {}
    a.show_list()
    while True:
        choice = input(f'Which donor would you like to edit?: ')
        if choice == 'quit':
            return
        for saved_donor in Donor:
            if choice == saved_donor.donor_name:
                query = (Donation.select().where(Donation.held_by == choice).order_by(Donation.dono_number))
                for ind in query:
                    print(f'Invoice: {ind.dono_number}: {ind.dono}')
                    new_dict[ind.dono_number] = ind.dono
#                print(new_dict)
                number = input(f'Which donation would you like to delete?: ')
                if number == 'quit':
                    return
#                print(new_dict.get(int(number)))
                inst = (Donation.select().where(Donation.held_by == choice, Donation.dono_number == number))
                for item in inst:
                    query = (Details.select().where(Details.name == choice).prefetch(Donor, Donation))
                    for ind in query:
                        ind.transactions -= 1
#                        print(ind.name.donations, float(item.dono))
                        ind.name.donations = (float(ind.name.donations) - float(item.dono))
                        ind.average = (ind.name.donations / ind.transactions)
                        item.delete_instance()
                        num = (Donation.select(fn.MAX(Donation.dono_number)).where(Donation.held_by == choice).scalar())
                        replacing = (Donation.select().where(Donation.dono_number == num))
                        for number in replacing:
                            ind.last_gift = number.dono
                        ind.save()
                        ind.name.save()
#                        print(ind.name.donations)

#MAKE IT SO IF FIRST DONATION IS DELETED, A NEW FIRST DONATION TAKES ITS PLACE. SAME WITH LAST DONATION.
                        
#                query = (Donation.select().where(Donation.held_by == choice).order_by(Donation.dono_number))
#                for ind in query:
#                    print(f'{ind.dono_number}: {ind.dono}')
                    
                return
        print('\nDonator does not exist.\n')
        continue
        
def edit():
    new_dict = {}
    a.show_list()
    while True:
        choice = input(f'Which donor would you like to edit?: ')
        if choice == 'quit':
            return
        for saved_donor in Donor:
            if choice == saved_donor.donor_name:
                query = (Donation.select().where(Donation.held_by == choice).order_by(Donation.dono_number))
                for ind in query:
                    print(f'Invoice: {ind.dono_number}: {ind.dono}')
                    new_dict[ind.dono_number] = ind.dono
#                print(new_dict)
                number = input(f'Which donation would you like to edit?: ')
                if number == 'quit':
                    return
                replace = input(f'What is the correct donation amount?: ')
                if replace == 'quit':
                    return
                inst = (Donation.select().where(Donation.held_by == choice, Donation.dono_number == number))
                for item in inst:
                    query = (Details.select().where(Details.name == choice).prefetch(Donor, Donation))
                    for ind in query:
#                        print(ind.name.donations, float(item.dono))
                        ind.name.donations = (float(ind.name.donations) - float(item.dono) + float(replace))
                        ind.average = (ind.name.donations / ind.transactions)
                        item.dono = float(replace)
                        num = (Donation.select(fn.MAX(Donation.dono_number)).where(Donation.held_by == choice).scalar())
                        replacing = (Donation.select().where(Donation.dono_number == num))
                        for number in replacing:
                            ind.last_gift = number.dono
                        ind.save()
                        ind.name.save()
                        item.save()
                return
                    
                            
def thank_you():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        while True:
            donator_name = input('\nWhat is the name of the donor?: ')
            if donator_name == 'list':
                for saved_donor in Donor:
                    print(f'{saved_donor}')
                continue
            elif donator_name == 'quit':
                return
            while True:
                try:
                    donation = float(input('\nWhat is the donation amount?: '))
                    if donation > 150:
                        size = 'Large'
                    else:
                        size = 'Small'
                except ValueError:
                    print('\nPlease give a number instead.')
                    continue
                break
            num = (Donation.select(fn.MAX(Donation.dono_number)).scalar())
            for saved_donor in Donor:
                if donator_name == saved_donor.donor_name:
                    print('Existing donor - adding donation to database')
                    query = (Details.select().where(Details.name == donator_name).prefetch(Donor, Donation))
                    for ind in query:
                        print(ind.name.donations)
                        ind.transactions += 1
                        ind.name.donations = (donation + float(ind.name.donations))
                        ind.average = (ind.name.donations / ind.transactions)
                        ind.last_gift = donation
                        ind.save()
                        ind.name.save()
                    new_dono = Donation.create(
                        held_by=donator_name,
                        dono=donation,
                        dono_size=size,
                        dono_number=(num+1)
                        )
                    new_dono.save()
                    print(ind.name.donations)
                    return
            print('New donor - adding donor to database')
            new_donor = Donor.create(donor_name=donator_name, donations=donation)
            new_donor.save()
            new_details = Details.create(name=donator_name,
                transactions=1,
                average=donation,
                first_gift=donation,
                last_gift=donation
                )
            new_details.save()
            new_dono = Donation.create(
                held_by=donator_name,
                dono=donation,
                dono_size=size,
                dono_number=(num+1)
                )
            new_dono.save()
            return
            
    finally:
        database.close()

def quitting():
    """
    quits the program
    """
    sys.exit()

def continuing():
    """
    continues the program
    """
    print('Try Again.\n')
    
    
a = DonorCollection()

switch_func_dict = {
    '1':thank_you,
    '2':edit,
    '3':delete,
    '4':a.report,
    '5':a.letters,
    '6':a.save,
    '7':a.load,
    '8':show_donations,
    '9':quitting,
    'quit':quitting,
    'list':a.show_list
    }

if __name__ == '__main__':
    database = SqliteDatabase('mail_default.db')
    while True:
        choice = input(f'\n1: Add Donation' +\
        f'\n2: Edit Donation' +\
        f'\n3: Delete Donation' +\
        f'\n4: Create a Report' +\
        f'\n5: Send Letters to Everyone' +\
        f'\n6: Save' +\
        f'\n7: Load' +\
        f'\n8: Show Donations' +\
        f'\n9: Quit' +\
        f'\n\nChoose an Option: '
        )
        c = switch_func_dict.get(choice, continuing)()