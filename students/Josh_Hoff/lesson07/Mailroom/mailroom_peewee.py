"""
    Mailroom utilizing a database
"""
import sys
import logging
from .create_mailroom import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
        
class Donorhandle:
    def __init__(self, choice = '', number = None):
        if number != None:
            inst = (Donation.select().where(Donation.held_by == choice, Donation.dono_number == number))
            item = [i for i in inst][0]
            item.delete_instance()

        self.choice = choice
        self.query = (Donation.select().where(Donation.held_by == self.choice).order_by(Donation.dono_number))
        self.ind = (Details.select().where(Details.name == self.choice).prefetch(Donor, Donation))[0]
        self.max = (Donation.select(fn.MAX(Donation.dono_number)).where(Donation.held_by == self.choice).scalar())
        self.min = (Donation.select(fn.MIN(Donation.dono_number)).where(Donation.held_by == self.choice).scalar())
        self.query_max = (Donation.select().where(Donation.dono_number == self.max))
        self.query_min = (Donation.select().where(Donation.dono_number == self.min))

    @property
    def gifts(self):
        self.ind.transactions = len([i for i in self.query])
        self.ind.save()
        return self.ind.transactions
        
    @property
    def total_donations(self):
        self.ind.name.donations = sum([i.dono for i in self.query])
        self.ind.name.save()
        return self.ind.name.donations
        
    @property
    def average(self):
        try:
            self.ind.average = (self.ind.name.donations / self.ind.transactions)
        #removes a donor if the last donation of a donor is deleted
        except ZeroDivisionError:
            delete_user = (Donor.select().where(Donor.donor_name == self.choice))
            delete_user = [i for i in delete_user][0]
            delete_user.delete_instance()
        self.ind.save()
        return self.ind.average
        
    @property
    def recent_gift(self):
        for number in self.query_max:
            self.ind.last_gift = number.dono
        self.ind.save()
        return self.ind.last_gift
        
    @property
    def first_gift(self):
        for number in self.query_min:
            self.ind.first_gift = number.dono
        self.ind.save()
        return self.ind.first_gift
        
    @property
    def invoice(self):
        self.num = (Donation.select(fn.MAX(Donation.dono_number)).scalar())
        self.num.save()
        return self.num
        
def set_variables(choice, number = None):
    setting = Donorhandle(choice, number)
    setting.gifts
    setting.total_donations
    setting.average
    setting.recent_gift
    setting.first_gift
    
def modify_dono(choice, number, replace):
    inst = (Donation.select().where(Donation.held_by == choice, Donation.dono_number == number))
    item = [i for i in inst][0]
    item.dono = float(replace)
    item.save()
    
def new_donor(donator_name, donation, size, num):
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

def existing_donor(donator_name, donation, size, num):
    new_dono = Donation.create(
        held_by=donator_name,
        dono=donation,
        dono_size=size,
        dono_number=(num+1)
        )
    new_dono.save()
        
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
                number = input(f'Which donation would you like to delete?: ')
                if number == 'quit':
                    return
                set_variables(choice, number)                    
                return
        print('\nDonator does not exist.\n')
        continue
        
def edit():
    show_list()
    while True:
        choice = input(f'Which donor would you like to edit?: ')
        if choice == 'quit':
            return
        for saved_donor in Donor:
            if choice == saved_donor.donor_name:
                query = (Donation.select().where(Donation.held_by == choice).order_by(Donation.dono_number))
                check = [i.dono_number for i in query]
                for ind in query:
                    print(f'Invoice: {ind.dono_number}: {ind.dono}')
                while True:
                    number = input(f'Which donation would you like to edit?: ')
                    if number == 'quit':
                        return
                    elif int(number) not in check:
                        print('\nPlease type an invoice number from the list.\n')
                        continue
                    break
                replace = input(f'What is the correct donation amount?: ')
                if replace == 'quit':
                    return
                try:
                    float(replace)
                except ValueError:
                    print('\nPlease give a number instead.\n')
                    continue
                modify_dono(choice, number, replace)
                set_variables(choice)
                return
        print('\nPlease type a name from the list.\n')
        continue
                    
                            
def thank_you():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        while True:
            donator_name = input('\nWhat is the name of the donor?: ')
            if donator_name == 'list':
                show_list()
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
                    print('\nPlease give a number instead.\n')
                    continue
                break
            num = (Donation.select(fn.MAX(Donation.dono_number)).scalar())
            for saved_donor in Donor:
                if donator_name == saved_donor.donor_name:
                    print('Existing donor - adding donation to database')
                    existing_donor(donator_name, donation, size, num)
                    set_variables(donator_name)
                    return
            print('New donor - adding donor to database')
            new_donor(donator_name, donation, size, num)
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