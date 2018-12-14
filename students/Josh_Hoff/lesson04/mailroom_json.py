import sys
import copy
import pathlib
from json_save_meta import *

#this class handles all donor management
class Donor:
    def __init__(self, name = '', donations = None):
        self._donations = donations
        self._name = name
                
    @property
    def gifts(self):
        self._gifts = len(self._donations)
        return self._gifts
                
    @property
    def total_donations(self):
        self._total = sum(self._donations)
        return self._total
                
    @property
    def average(self):
        total = self.total_donations
        gifts = self.gifts
        self._average = round((total / gifts), 2)
        return self._average
                
    @property
    def recent_gift(self):
        self._recent_gift = self._donations[-1]
        return self._recent_gift
                
    @property
    def first_gift(self):
        self._first_gift = self._donations[0]
        return self._first_gift
        
        
class DonorCollection:
    
    def __init__(self):
        self._donors = {'Josh Hoff': [25, 75], 'Tatsiana Kisel': [35, 105.55]}
        
    @property
    def donors(self):
        return self._donors
        
    @donors.setter
    def donors(self, new_dict):
        self._donors = copy.deepcopy(new_dict)
        return self._donors

        
    def report(self):
        y = '|'
        rows = ''
        top = f'Donor Name{y:>14} Total Given {y} Num Gifts {y} Average Gift\n'
        top += ('-' * 63)
        sorted_donors = sorted(self._donors.items(), key=lambda k: sum(k[1]), reverse=True)
        for name, donations in sorted_donors:
            d = Donor(name, donations)
            gift = d.gifts
            total_donations = d.total_donations
            average = d.average
            rows += f'\n{name:<23} $ {total_donations:>11.2f} {gift:>11} {average:>11.2f}'
        top += rows
        print(f'\n{top}')
        
    def letters(self):
        tab = '    '
        for name, val in self._donors.items():
            with open(f'{name}.txt', 'w') as outfile:
                d = Donor(name, val)
                donation = d.total_donations
                val = self._donors.get(name)[-1]
                outfile.write(f'Dear {name}, \n\n{tab}Thank you very much for your most recent donation \
of ${val:.2f}! \n\n{tab}You have now donated a total of ${donation:.2f}. \n\n{tab}Your support \
is essential to our success and will be well utilized. \n\n{tab*2}Sincerely, \n{tab*3}-The Company')
    
    def show_list(self):
        print('')
        for i in self._donors:
            print(i)

    def add_donor(self, donor_name='Jacob', donation=30):
        if donor_name in self._donors:
            self._donors[donor_name] += [donation]
        else:
            self._donors[donor_name] = [donation]
        return self._donors
        
    def save(self):
        print('\nSaving...')
        self.mc = MyClass(self._donors)
        self.jc = self.mc.to_json_compat()
        save_file = json.dumps(self.jc)
        with open(f'save.txt', 'w') as outfile:
            outfile.write(save_file)
        
    def load(self):
        print('\nLoading...')
        with open(f'save.txt', 'r') as outfile:
            load_file = json.loads(outfile.read())
        self._donors = load_file['x']
        
class Functions:

    def __init__(self):
        pass
    
    @classmethod
    def challenge(cls, factor, min_donation=0, max_donation=9999999999999999999):
#        global donors
        modified_donors = copy.deepcopy(a._donors)
        lower_donors = copy.deepcopy(a._donors)
        higher_donors = copy.deepcopy(a._donors)

        for name in a._donors:
            modified_donors[name] = list(filter(lambda x : x > min_donation, modified_donors[name]))
            modified_donors[name] = list(filter(lambda x : x < max_donation, modified_donors[name]))
            
            lower_donors[name] = list(filter(lambda x : x < min_donation, lower_donors[name]))            
            higher_donors[name] = list(filter(lambda x : x > max_donation, higher_donors[name]))
            
        for name in a._donors:
            modified_donors[name] = list(map(lambda x : x*factor, modified_donors[name]))
            
        for name in a._donors:
            modified_donors[name] += lower_donors[name]
            modified_donors[name] += higher_donors[name]
            
#        print(modified_donors)
        return modified_donors
        
    @classmethod
    def projections(cls):
#        global donors
        d = Functions()
        x = d.challenge(2, 0, 100)
        y = d.challenge(3, 50)
        message = ('-' * 43)
        message += f'\nCurrent donations:\n'
        for name in a._donors:
            message += f'{name}: ${sum(a._donors[name])}\n'
        message += f'\nIf you double contributions under $100:\n'
        for name in a._donors:
            message += f'{name}: ${sum(x[name])}\n'
        message += f'\nIf you triple contributions over $50:\n'
        for name in a._donors:
            message += f'{name}: ${sum(y[name])}\n'
        message += ('-' * 43)
        print(message)
        
class MyClass(JsonSaveable):

    x = Dict()

    def __init__(self, x):
        self.x = x
        
        
def thank_you():
    while True:
        donor_name = input('\nWhat is the name of the donor?: ')
        if donor_name == 'list':
            a.show_list()
            continue
        elif donor_name == 'quit':
            return
        while True:
            try:
                donation = float(input('\nWhat is the donation amount?: '))
            except ValueError:
                print('\nPlease give a number instead.')
                continue
            break
        a.donors = a.add_donor(donor_name, donation)
        return
        
def quitting():
    sys.exit()
    
def continuing():
    print('Try Again.\n')
    

a = DonorCollection()
    
switch_func_dict = {'1':thank_you, '2':a.report, '3':a.letters, '4':Functions().projections, '5':a.save, '6':a.load, '7':quitting, 'quit':quitting, 'list':a.show_list}

#main function: adjusted to use classes
if __name__ == '__main__':
    while True:
        choice = input('\n1: Send a Thank You \n2: Create a Report \n3: Send Letters to Everyone \n4: Projections \n5: Save \n6: Load \n7: Quit \nChoose an Option: ')
        c = switch_func_dict.get(choice, continuing)()