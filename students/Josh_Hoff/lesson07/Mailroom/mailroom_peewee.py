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
        pass
            
    def save(self):
        pass

    def load(self):
        pass
        
    def report(self):
        pass
        
    def letters(self):
        pass
    

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
                except ValueError:
                    print('\nPlease give a number instead.')
                    continue
                break
            for saved_donor in Donor:
                if donator_name == saved_donor.donor_name:
                    print('Existing donor - adding donation to database')
                    query = (Details.select(Details, Donor).join(Donor).where(Details.name == donator_name))
                    for ind in query:
                        ind.transactions += 1
                        ind.total = (donation + float(ind.total))
                        ind.average = (ind.total / ind.transactions)
                        ind.last_gift = donation
                        ind.save()
                    return
            print('New donor - adding donor to database')
            new_donor = Donor.create(donor_name=donator_name, donations=donation)
            new_donor.save()
            new_details = Details.create(name=donator_name,
                transactions=1,
                total=donation,
                average=donation,
                first_gift=donation,
                last_gift=donation
                )
            new_details.save()
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
    '2':a.report,
    '3':a.letters,
    '4':a.save,
    '5':a.load,
    '6':quitting,
    'quit':quitting,
    'list':a.show_list
    }

if __name__ == '__main__':
    database = SqliteDatabase('mail_default.db')
    while True:
        choice = input(f'\n1: Send a Thank You' +\
        f'\n2: Create a Report' +\
        f'\n3: Send Letters to Everyone' +\
        f'\n4: Save' +\
        f'\n5: Load' +\
        f'\n6: Quit' +\
        f'\nChoose an Option: '
        )
        c = switch_func_dict.get(choice, continuing)()