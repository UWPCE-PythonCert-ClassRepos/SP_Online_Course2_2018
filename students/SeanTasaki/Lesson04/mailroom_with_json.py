#!/usr/bin/env python3
"""
Sean Tasaki
11/1/2018
Lesson04
"""
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter
import sys
import functools
import json
import json_save.json_save_dec as js



# Input functions
def main_menu(dc):
    main_menu_dict = {'1': dc.thank_you, 
                      '2': dc.create_report, 
                      '3': dc.create_thank_you_letters, 
                      '4': dc.match_contributions,
                      '5': dc.save_json,
                      '6': dc.load_json,
                      '7': dc.search_for_donor, 
                      '8': quit}
    main_prompt = "Enter 1-8 from the following options:\n\
                   (1) Send a Thank You to a Donor\n\
                   (2) Create a Report\n\
                   (3) Write a Thank You Letter to All Donors\n\
                   (4) Match Contributions\n\
                   (5) Save to Json file\n\
                   (6) Load from Json file\n\
                   (7) Search for a Donor\n\
                   (8) Quit\n\
                   >> "  
    main_menu_response(main_prompt, main_menu_dict)

def main_menu_response(prompt, main_menu_dict):
    while True:
        response = input(prompt)
        try:
            if main_menu_dict[response]() == "exit menu":
                sys.exit(0)
        except KeyError:
            print("Enter a number between 1-5.")    

def quit():
    return 'exit menu'

def donor_name_prompt():
    return input('Enter the first and last name of the donor or enter ''list'' to see a list of previous donor names or enter Q to exit to main menu\n> ')          

def donation_prompt():
     return float(input("Please enter the donation amount:\n"))

def projection_prompt():
    return int(input('Enter 0 for an estimate or 1 to match contributions:\n>'))
def factor_prompt():
    return int(input('Enter the factor to match contributions:\n>'))

def min_amount_prompt():
    return float(input('Enter minimum donation amount to match:\n>'))

def max_amount_prompt():
    return float(input('Enter maximum donation amount to match:\n>'))

@js.json_save
class Donor():

    _first = js.String()
    _last = js.String()
    _donations = js.List()

    def __init__(self, first_name, last_name, donations = None):
        self._first = first_name
        self._last = last_name
        if donations is None:
            self._donations = []
        else:
            self._donations = donations

    @property
    def full_name(self):
        return '{} {}'.format(self._first, self._last)


    def thank_you_letter_template(self, donor):
        if self.num_of_donations > 1:
            return "Dear {},\nThank you for your {} generous donations of ${:.2f}. Your continued support helps our charity stay in business.\n\nSincerely,\n-The Team\n".format(donor.full_name, donor.num_of_donations, donor.total_donation)
        else:
            return "Dear {},\nThank you for your generous donation of ${:.2f}. Your support helps our charity stay in business.\n\nSincerely,\n-The Team\n".format(donor.full_name, donor.total_donation)


    def add_donation(self, amount):
        return self._donations.append(amount)

    @property
    def num_of_donations(self):
        return len(self._donations)

    @property
    def total_donation(self):
        return sum(self._donations)

    @property
    def avg_donation(self):
        return sum(self._donations/ len(self._donations))

    @property
    def donation_lis(self):
        return self._donations  

    def __str__(self):
        return f"{self.full_name:20} ${self.total_donation:>17.2f}    {self.num_of_donations:>6}     ${self.avg_donation:>16.2f}" 

@js.json_save
class DonorCollection:
    #convert list to json
    donorsdict = js.Dict()

    def __init__(self, donors):
        self.donorsdict = donors
    
    def add_donor(self, donor):
        return self.donorsdict.update({donor.full_name: donor.donation_lis})

    #Returns sorted list of all donors
    def get_all_donors(self):
       donor_lis = list(self.donorsdict.keys())
       return sorted(donor_lis)

    def search_for_donor(self):
        reply = input("Enter first and last name of donor>> ")
        donor = reply.title()
        if donor not in self.donorsdict:
            print("{} is not a previous donor.".format(donor))
        else:
            for key, val in self.donorsdict.items():
                if donor == key:
                    print("Name: {}\nDonations: {}\n".format(donor, val))    
        

    def sort_donors_by_total_amount(self):
        donor_total_amount = {key:sum(value) for key, value in self.donorsdict.items()}
        return OrderedDict(sorted(donor_total_amount.items(), key = itemgetter(1), reverse = True))
    
    def thank_you(self):
        try:
            self.name = donor_name_prompt()            
            if self.name.lower() == 'list':
                print(self.get_all_donors())
            elif self.name.upper() == 'Q':
                main_menu(self)
            first, last = self.name.split(' ')
        except ValueError:
            print("Invalid input.")
            self.thank_you()               
        else: 
            success = False
            while not success:   
                try:
                    self.donation = donation_prompt()
                    success = True

                except ValueError:
                    print('Please enter a valid number.')
                    success = False

            self.donor = Donor(first.title(), last.title(), [self.donation])
            
            if self.donor.full_name not in self.donorsdict:
                print(f"{self.name.title()} is a new donor.")
                print(self.thank_you_message(self.name, self.donation, 0))
                self.add_donor(self.donor)
            else:
                print(f"{self.name.title()} is a previous donor.\n>> ")          
                print(self.thank_you_message(self.name, self.donation, 1))
                self.donorsdict[f"{first.title()} {last.title()}"].append(self.donation)
        

    def thank_you_message(self, name, donation, type):
        #New donor message
        if type == 0:
            return f"Thank you {name.title()} for becoming a new donor to our charity! Your genereous donation of ${float(donation):.2f} is much appreciated."
        # previous donor message   
        elif type == 1:
            return f"Thank you {name.title()} for your loyal support to our charity! Your genereous donation of ${float(donation):.2f} is much appreciated."  
    
    def match_contributions(self, projection = -1):
        while projection not in [0, 1]:
            try:
                projection = projection_prompt()
            except ValueError:
                print('invalid input')
        
        success = False
        while not success or min_amount > max_amount:   
            try:
                factor = factor_prompt()
                min_amount = min_amount_prompt()
                max_amount = max_amount_prompt()
                if min_amount > max_amount:
                    print('The minimum donation amount must be less than the maximum donation amount')   
                else:               
                    success = True

            except ValueError:
                print('Please enter a valid number.')
                success = False
       
        self.challenge(projection, min_amount, max_amount, factor)
        

    def challenge(self, projection = 0, min = 0, max = 99999999, factor = 1):
        #Multiplies  total donation amount of each donor by factor.
        total = 0
        for donor in self.donorsdict:
            filtered_list1 = list(filter(lambda x: x >= min and x <= max, self.donorsdict[donor]))
            filtered_list2 = list(filter(lambda x: x < min and x > max, self.donorsdict[donor]))
            challenge_list = list(map(lambda x: x * factor, filtered_list1))
            if projection == 1:
                self.donorsdict[donor] = challenge_list + filtered_list2
            else:
                if challenge_list:                      
                    total = total + functools.reduce(lambda x, y: x + y, challenge_list)
                
        if projection == 1:
            print(f"All donations have been multiplied by a factor of {factor}")
            return self.donorsdict  
        else:
            if total == 0:             
                print('There were no donation amounts that fit into the range of minimum and maximum donations. Please re-adjust minimum and maximum donations.')
            else:
                print(f'Total estimated donation: ${total:.2f}')

    
    def create_report(self):     

        print("Donor Name           |   Total Given   |   Num Gifts  |    Average Gift")
        print("-----------------------------------------------------------------------")
        
        for donor in self.sort_donors_by_total_amount():
            print(f"{donor:20} ${sum(self.donorsdict.get(donor)):>17.2f}    {len(self.donorsdict.get(donor)):>6}     ${sum(self.donorsdict.get(donor))/ len(self.donorsdict.get(donor)):>16.2f}")  
        

    def create_thank_you_letters(self):
        # Creates a letter for each donor that gets a file in the working dir based on donor's name.
        for donor in self.donorsdict:
            letter = self.letter_template(donor)
            with open(donor + ".txt",'w') as output:
                output.write(letter)
        print("Letters have been generated.")

    
    def letter_template(self, donor):
        letter = "Dear {},\n   Thank you for donating ${:,.2f}. Your donation makes a positive impact on your community.\n\nSincerely,\nThe Team".format(donor, sum(self.donorsdict.get(donor)))
        return letter

    def thank_you_email_template(self, dk):
        if len(self.donorsdict.get(dk)) > 1:
            return "Dear {},\nThank you for your {} generous donations of ${:.2f}. Your support helps our charity stay in business.\n\nSincerely,\n-The Team".format(dk, len(self.donorsdict.get(dk)), sum(self.donorsdict.get(dk)))
        else:
            return "Dear {},\nThank you for your generous donation of ${:.2f}. Your support helps our charity stay in business.\n\nSincerely,\n-The Team".format(dk, sum(self.donorsdict.get(dk)))

    def save_json(self):
        """Saves the donor dictionary into a json file"""
        json_string = json.dumps(self.to_json_compat())
        with open('Donor_DB.json', 'w') as file:
            file.write(json_string)
        print("Your file has been generated.")

    def load_json(self):
        """Loads donor information from a json file"""
        with open('Donor_DB.json','r') as data_load:
            json_data = json.load(data_load)
        self.donorsdict = self.from_json_dict(json_data).donorsdict
        print("Donors have been loaded.")


if __name__ == '__main__':
    donor_dict = defaultdict(list, {'Bob Dylan': [2000.00, 500.00, 3.00], 'Italo Calvino': [1001.00, 333.00], 'Feist Scotia': [1500.00, 30.00]})
    dc = DonorCollection(donor_dict)
    main_menu(dc)


