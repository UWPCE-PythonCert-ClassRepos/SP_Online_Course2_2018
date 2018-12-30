"""
    Mailroom utilizing a database
"""
import sys
import logging
from create_mailroom import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
        
def show_list():
    for saved_donor in Donor:
        print(f'{saved_donor}')
    return
                    
def report():
    donorq = (Donor.select().order_by(Donor.donor_name)).prefetch(Donation)
    for i in donorq:
        print(i.donor_name)
        for x in i.name_person:
            print(f'  Invoice: {x.dono_number} : ${x.dono}')
        print(f'  Total Donations: ${i.donations}')
        for x in i.person_name:
            print(f'   Transactions - {x.transactions}')
            print(f'   Average Donation - ${x.average:.2f}')
            print(f'   First Donation - ${x.first_gift}')
            print(f'   Latest Donation - ${x.last_gift}')
        
def letters():
    tab = '    '
    query = (Details.select().order_by(Details.name)).prefetch(Donor)
    for name in query:
        with open(f'{name.name.donor_name}.txt', 'w') as outfile:                
            donation = name.name.donations
            val = name.last_gift
            outfile.write(f'Dear {name.name.donor_name}, \n\n{tab}Thank you very much for your most recent donation \
of ${val:.2f}! \n\n{tab}You have now donated a total of ${donation:.2f}. \n\n{tab}Your support \
is essential to our success and will be well utilized. \n\n{tab*2}Sincerely, \n{tab*3}-The Company')
    
def show_donations():
    show_list()
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
    show_list()
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
                        max = (Donation.select(fn.MAX(Donation.dono_number)).where(Donation.held_by == choice).scalar())
                        min = (Donation.select(fn.MIN(Donation.dono_number)).where(Donation.held_by == choice).scalar())
                        query_max = (Donation.select().where(Donation.dono_number == max))
                        query_min = (Donation.select().where(Donation.dono_number == min))
                        for number in query_max:
                            ind.last_gift = number.dono
                        for number in query_min:
                            ind.first_gift = number.dono
                        ind.save()
                        ind.name.save()                        
#                query = (Donation.select().where(Donation.held_by == choice).order_by(Donation.dono_number))
#                for ind in query:
#                    print(f'{ind.dono_number}: {ind.dono}')
                    
                return
        print('\nDonator does not exist.\n')
        continue
        
def edit():
    new_dict = {}
    show_list()
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
                        item.save()
                        max = (Donation.select(fn.MAX(Donation.dono_number)).where(Donation.held_by == choice).scalar())
                        min = (Donation.select(fn.MIN(Donation.dono_number)).where(Donation.held_by == choice).scalar())
                        query_max = (Donation.select().where(Donation.dono_number == max))
                        query_min = (Donation.select().where(Donation.dono_number == min))
                        for number in query_max:
                            ind.last_gift = number.dono
                        for number in query_min:
                            ind.first_gift = number.dono
                        ind.save()
                        ind.name.save()
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

switch_func_dict = {
    '1':thank_you,
    '2':edit,
    '3':delete,
    '4':report,
    '5':letters,
    '6':show_donations,
    '7':quitting,
    'quit':quitting,
    'list':show_list
    }

if __name__ == '__main__':
    database = SqliteDatabase('mail_default.db')
    while True:
        choice = input(f'\n1: Add Donation' +\
        f'\n2: Edit Donation' +\
        f'\n3: Delete Donation' +\
        f'\n4: Create a Report' +\
        f'\n5: Send Letters to Everyone' +\
        f'\n6: Show Donations' +\
        f'\n7: Quit' +\
        f'\n\nChoose an Option: '
        )
        c = switch_func_dict.get(choice, continuing)()