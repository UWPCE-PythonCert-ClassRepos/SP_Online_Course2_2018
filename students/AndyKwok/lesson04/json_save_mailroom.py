# Description: Mailroom Program - Json
# Author: Andy Kwok
# Last Updated: 11/23/18
# ChangeLog: 
# v1.0 - Initialization, with source code from 
#           mailroom_oo.py, mailroom_fp.py 
#           and mailroom_pt9.py

#!/usr/bin/env python3

import json_save_meta as json

class Mailroom(json.JsonSaveable):
    name = json.String()
    donorlist = json.List()
    
    def __init__(self, name=None, donorlist=None):
        self.name = name
        self.donorlist = donorlist
    
    @property
    def save(self):
        mailroom_saved = self.to_json()
        with open('mailroom.json', 'w') as file:
            file.write(mailroom_saved) 
        print('Mailroom database saved as mailroom.json....')
    
    @property
    def load(self):
        with open('mailroom.json', 'r') as file:
            mailroom_loaded = json.from_json(file.read())
        return mailroom_loaded

    @property
    def sort(self):
        self.donorlist.sort()
    
    @property
    def display_all(self):
        if self.donorlist[0].name is not None:
            self.sort
        for i in self.donorlist:
            i.display
    @property
    def letter_all(self):
        for i in self.donorlist:
            i.letter

    def add_donor(self, donor_name, amount):
        if self.donorlist[0].name is None:
            self.donorlist[0].name = donor_name
            self.donorlist[0].donation = [amount]
        else:
            if donor_name not in [x.name for x in self.donorlist]:
                self.donorlist += [Donor(donor_name, [amount])]
            else:
                i = [x.name for x in self.donorlist].index(donor_name)
                self.donorlist[i].donation += [amount]
    
class Donor(json.JsonSaveable):
    name = json.String()
    donation = json.List()
    
    def __init__(self, name=None, donation=None):
        self.name = name
        self.donation = donation

    def __lt__(self, other):
        return self.name < other.name
        
    @property
    def average(self):
        return sum(self.donation)/len(self.donation)
    
    @property
    def total(self):
        return sum(self.donation)
       
    @property
    def display(self):
        print('{:20}'.format(self.name) +
                '$ {:>10.2f} {:7}'.format(self.total, len(self.donation)) +
                ' '*14 + '$ {:>10.2f}'.format(self.average))

    @property
    def letter(self):
        content = ('To {},\n'.format(self.name) +
                    'Thank you for your donation of ${:.2f}.'.format(self.total) +
                    '\n'*2 + '\t'*5 + '-System Generated Email')
        with open(self.name + '.txt', 'w') as text:
            text.write(content)

    def add_donation(self, amount):
        self.donation.append(amount)
        
class Menu:
    
    def __init__(self, data):
        self.data = data
        self.one = {1: self.add_entry,
                    2: self.report,
                    3: self.sent_letter,
                    4: self.save_db,
                    5: self.load_db,
                    6: self.quit
                    }
    
    def main(self):
        print("="*75)
        print(
            '''    
            1 - Add a Donation
            2 - Report Out
            3 - Automated Letters
            4 - Save Database
            5 - Load Database
            6 - Quit
            '''
            )
        print("="*75)
        option = int(input('Please select an option> '))
        return self.one[option]()
        
    def save_db(self):
        self.data.save
        return 'cont'
        
    def load_db(self):
        self.data = self.data.load
        return 'cont'
        
    def report(self):
        print('Donor Name' + ' '*10 + '| Total Given' + ' '*5 + '| Num Gifts' + ' '*5 + '| Average Gift')
        print('-'*75)
        self.data.display_all
        return 'cont'

    def sent_letter(self):
        self.data.letter_all
        return 'cont'
    
    def add_entry(self):
        id = input('Name of the donor: ')
        try:
            amount = float(input('Amount of donation: '))
        except ValueError:
            print("Please enter a real donation amount.")        
        self.data.add_donor(id, amount)
        return 'cont'
        
    def quit(self):
        return 'end'


if __name__ == "__main__":
    # database = Mailroom('Mailroom A',
                        # [Donor('Donor C', [3.0]),
                        # Donor('Donor A', [1, 3, 5]),
                        # Donor('Donor B', [10, 20])])

    database = Mailroom(None,[Donor(None)])
    main_menu = Menu(database)
    select = None
    while select != 'end':
        select = main_menu.main()