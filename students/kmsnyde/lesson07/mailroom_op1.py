# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 12:20:46 2018

@author: HP-Home
"""
import logging

from sys import exit
from mailroom_sql import *
from peewee import *


class Main:
    def __init__(self):
        self.menu = {1: 'Send a Thank You (and add/update donor)',
                     2: 'Create a Report',
                     3: 'Send letters to everyone',
                     4: 'Delete a Donor',
                     5: 'Quit'}
    
    def main_menu(self):
        print('\n', 'Please select a number from the following choices:\n')
        return {(print(str(k) + ':', v)) for k, v in self.menu.items()}
    
    def selection(self):
        while True:
            input1 = input("Selection: ")
            try:
                if int(input1) in range(1, 5):
                    if int(input1) == 1:
                        print('\nType a user\'s name or "list" to show names.')
                        input2 = input('-> ')
                        if input2 == 'list':
                            query = (Donor.select(Donor, fn.COUNT(Donation.id).alias('donation_count')).join(Donation, 
JOIN.LEFT_OUTER).group_by(Donor).order_by(Donor.username))
                            for i in query:
                                print(i.username)
                            Main()
                            self.main_menu()
                            self.selection()
                        else:
                            input3 = input('Donation amount: ')
                            try:
                                new_user = Donor.create(username=input2)
                                Donation.create(user=new_user, donation=float(input3))
                                self.send_thanks(input2, input3)
                            except IntegrityError:
                                update_rec = Donation.create(user=input2, donation=float(input3))
                                update_rec.save()
                                Main()
                                self.main_menu()
                                self.selection()
                            
                    elif int(input1) == 2:
                        self.create_report()
                    elif int(input1) == 3:
                        self.send_letters_all()
                    elif int(input1) == 4:
                        self.delete_donor()
                elif int(input1) == 5:
                    print("Exiting program...")
                    raise SystemExit()
                    #break
            except ValueError:
                print("You must use a menu number between 1-4; try again!")
                
    def send_thanks(self, name, amount):
        letter = 'Thank you {} for your donation in the amount of ${}; it is very generous.'.format(name, amount)
        with open('Thank_You - {}.txt'.format(name.lower().
                     replace(' ', '_')), 'w') as f:
            f.write(letter)
        print("Your thank you letter has been written to disk.")
        
    def create_report(self):
        print('\n{:<20} {:>20} {:>20} {:>20}'.format('Donor Name',
              '| Total Given', '| Num Gifts', '| Average Gift'))
        print('{}'.format('-' * 83))
        
        report = (Donor.select(Donor, fn.Sum(Donation.donation).alias('sum'), fn.Count(Donation.id).alias('count'), fn.AVG(Donation.donation).alias('avg')).join(Donation).group_by(Donor).order_by(fn.Sum(Donation.donation).desc()))
        
        for i in report:
            print('{:<20} {:>20.02f} {:>20} {:>20.02f}'.format(i.username, i.sum, i.count, i.avg))
            
        Main()
        self.main_menu()
        self.selection()
            
    def send_letters_all(self):
        
        letters = 'Dear {},\n\n\tThank you for your total contributions in the amount of ${}.\n\n\tYou are making a difference in the lives of others.\n\n\t\tSincerely,\n\t\t"Working for America"'
        
        report = (Donor.select(Donor, fn.Sum(Donation.donation).alias('sum'), fn.Count(Donation.id).alias('count'), fn.AVG(Donation.donation).alias('avg')).join(Donation).group_by(Donor).order_by(fn.Sum(Donation.donation).desc()))
        
        for i in report:
           with open('Thank_You_Letter - {}.txt'.format(i.username.lower().replace(' ', '_')), 'w') as f:
               f.write(letters.format(i.username, i.sum))
        print('\nYour letters have been printed to the current directory!')
        
        Main()
        self.main_menu()
        self.selection()
        
    def delete_donor(self):
        print('\nType a user\'s name or "list" to show names.')
        input2 = input('-> ')
        if input2 == 'list':
            names = (Donor.select(Donor, fn.COUNT(Donation.id).alias('donation_count')).join(Donation, 
JOIN.LEFT_OUTER).group_by(Donor).order_by(Donor.username))
            for i in names:
                print(i.username)
            Main()
            self.main_menu()
            self.selection()
        else:
            user = Donor.get(Donor.username == input2)
            user.delete_instance()
            print(f'You deleted {input2} from the donor database.')
            Main()
            self.main_menu()
            self.selection()
            
    def goodbye():
        logger.info('database is closing...')
        database.close()
        sys.exit()
        
def initialize():
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('The next 3 lines of code are the only database specific code')
    database = SqliteDatabase('donor.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    database.drop_tables([Donor, Donation])
    Donor()
    Donation()
    populate_db()


                
if __name__ == '__main__':
    initialize()
    ex = Main()
    ex.main_menu()
    ex.selection()
    