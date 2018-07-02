# -*- coding: utf-8 -*-
"""
Created on Sun May 20 07:03:34 2018

@author: Karl M. Snyder
"""

import json
import json_save_dec as jsd 
from saveables import List, Dict

class Main:
    def __init__(self):
        self.menu = {1: 'Send a Thank You',
                     2: 'Create a Report',
                     3: 'Send letters to everyone',
                     4: 'Read json data from file',
                     5: 'Quit'}
    
    def main_menu(self):
        print('\n', 'Please select a number from the following choices:\n')
        return {(print(str(k) + ':', v)) for k, v in self.menu.items()}
    
    def selection(self):
        while True:
            input1 = input("Selection: ")
            #print(type(input1), input1)
            try:
                if int(input1) in range(1, 5):
                    if int(input1) == 1:
                        print('\nType a user\'s name or "list" to show names.')
                        input2 = input('-> ')
                        if input2 == 'list':
                            our_donors.donors()
                            continue
                        else:
                            input3 = input('Donation amount: ')
                            user = Donor(input2, input3)
                            user.send_thanks()
                    if int(input1) == 2:
                        our_donors.create_report()
                    if int(input1) == 3:
                        our_donors.send_letters_all()
                    if int(input1) == 4:
                        print("selected 4")
                        print(our_donors.js_data)
                elif int(input1) == 5:
                    print("Exiting program...")
                    break
            except ValueError:
                print("You must use a menu number between 1-4; try again!")

class Donor:
    
    donor_dict = Dict()
    donation_list = List()
    
    def __init__(self, name, donations):
        self.name = name
        self.donor_dict = {}
        self.donation_list = []
        
        if type(donations) == int or type(donations) == float: 
            self.donation_list.append(round(donations, 2))
        elif type(donations) == list:
            for i in donations:
                self.donation_list.append(round(i, 2))
        else:
            raise ValueError('You must enter a number for donation amount.')
            
        self.donor_dict = {'name': self.name, 'donations': self.donation_list}
        
        
        self.sum_dict = {'name': self.name,
                        'total': round(sum(self.donation_list, 2)),
                         "num_donations": len(self.donation_list),
                         "avg": round(sum(self.donation_list) / len(self.donation_list), 2)}
        
     
    def append(self, amount):
        self.donation_list.append(amount)
        self.donation_list
        
        self.sum_dict = {'name': self.name,
                        'total': round(sum(self.donation_list, 2)),
                         "num_donations": len(self.donation_list),
                         "avg": round(sum(self.donation_list) / len(self.donation_list), 2)}
        with open('donor_data.json', 'w') as f:
            data = json.dumps(self.sum_dict)
            f.write(data)
            
        d.add(self.name.lower(), self.sum_dict)
            

    
    @property
    def avg(self):
        return round(sum(self.donation_list, 2) / len(self.donation_list))
    
    @property
    def total(self):
        return round(sum(self.donation_list))
    
    @property
    def status(self):
        return (self.name, self.total, len(self.donation_list), self.avg)
    
    def send_thanks(self):
        letter = 'Thank you {} for your donation in the amount of ${}; it is very generous.'.format(self.name, self.donation_list[-1])
        with open('Thank_You - {}.txt'.format(self.name.lower().
                     replace(' ', '_')), 'w') as f:
            f.write(letter)
        print("Your thank you letter has been written to disk.")
        
    def __repr__(self):
        return repr(self.donor_dict)
   

class Donors:
    
    donors = Dict()
    
    def __init__(self, name, donor ):
        self.donors = {}
        self.donors[name] = {}
        self.donors[name].update(donor)

    def add(self, name, donor):
        self.donors[name] = donor
        return self.donors
        
    def save_json(self):
        with open('database.json', 'w') as f:
            json.dump(self.donors, f)
            
    def open_json(self):
        with open('database.json', 'r') as f:
            database = json.load(f)
            print(database)

    def __repr__(self):
        return repr(self.donors)
    
    @property
    def names(self):
        for k, v in self.donors.items():
            print(v['name'])
    
    @property        
    def key(tup):
        key, d = tup
        return d.donors['total']
    
    @property
    def data_sort(self):
        return sorted(self.donors.items(), key=lambda x: x[1]['total'], 
                      reverse=True)

    letters = 'Dear {},\n\n\tThank you for your total contributions in the amount of ${}.\n\n\tYou are making a difference in the lives of others.\n\n\t\tSincerely,\n\t\t"Working for America"'

    def create_report(self):
        print('\n{:<20} {:>20} {:>20} {:>20}'.format('Donor Name',
              '| Total Given', '| Num Gifts', '| Average Gift'))
        print('{}'.format('-' * 83))
        
        for k,v in self.data_sort:
            print('{:<20} {:>20.02f} {:>20} {:>20.02f}'.format(v['name'], v['total'], v['num_donations'], v['avg'])) 
        
    def send_letters_all(self):
        for k,v in self.data_sort:
           with open('Thank_You - {}.txt'.format(v['name'].lower().replace(' ', '_')),
                     'w') as f:
               f.write(self.letters.format(v['name'], v['total']))
        print('\nYour letters have been printed to the current directory!')
        
if __name__ == '__main__':
    karl = Donor('Karl', [100, 200, 300])
    bob = Donor('Bob', [400, 500, 600])
    woody = Donor('Woody', [700, 800, 900])
    d = Donors('karl', karl.sum_dict)
    d.add('bob', bob.sum_dict)
    d.add('woody', woody.sum_dict)
    d.create_report()
    d.save_json()
    d.open_json()
    bob.append(250)
    karl.append(350)
    bob.send_thanks()
    d.create_report()
    d.send_letters_all()
    d.save_json()
    d.open_json()
    
