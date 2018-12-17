#!/usr/bin/env python3
"""
Sean Tasaki
11/14/2018
Lesson07
"""
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter
import sys
import functools
from peewee import *
import mailroom_database
from mailroomdb_queries import *
import logging



# Input functions
def main_menu(dc):
    main_menu_dict = {'1': dc.thank_you, 
                      '2': dc.create_report, 
                      '3': dc.create_thank_you_letters, 
                      '4': dc.match_contributions,
                      '5': dc.delete_donor,
                      '6': dc.update_donor,
                      '7': dc.display_result_of_donor_search, 
                      '8': quit}
    main_prompt = "Enter 1-8 from the following options:\n\
                   (1) Add a Donor\n\
                   (2) Create a Report\n\
                   (3) Write a Thank You Letter to All Donors\n\
                   (4) Match Contributions\n\
                   (5) Delete Donor\n\
                   (6) Update Donor\n\
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
            print("Enter a number between 1-8.")    

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


class Donor():    

    def __init__(self, first_name, last_name):
        self._first = first_name
        self._last = last_name
        self.id_num = 0
    
    @property
    def full_name(self):
        return '{} {}'.format(self._first, self._last)

    @property
    def id_num(self):
        return self.__id_num

    @id_num.setter
    def id_num(self, num):
        self.__id_num = num

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

class DonorCollection:

    def __init__(self, donors, dbqueries):
        self.donorsdict = donors
        self.dbqueries = dbqueries
    

    #Returns sorted list of all donors
    def get_all_donors(self):
        self.dbqueries.print_donors(self.donorsdict)
       #donor_lis = list(self.donorsdict.keys())
       #return sorted(donor_lis)

    def search_for_donor(self):
        while True:
            reply = input("Enter first and last name of donor or enter 'Q' to return to main menu>> ")
            if reply.upper() == 'Q':
                main_menu(self)
            try:
                first, last = reply.split(' ')
                query = self.dbqueries.search_donor(first, last)
            except ValueError:
                print("Invalid input. Must enter a first and last name only.")
                continue
     
            if query:
                query_tuple = query.tuples()
                logging.info(f'searh_for_donor: {query_tuple}')
                return reply, query_tuple
            else:
                print("Donor not found! Please try again.")


    def display_result_of_donor_search(self):
        reply, query_tuple= self.search_for_donor()
        self.dbqueries.display_single_donor(reply, query_tuple)

    def update_donor(self):
        reply, query = self.search_for_donor()
        self.dbqueries.update_donor_query(query)


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
            logging.info(f'printing 164 {self.name.title()}')
            self.query = self.dbqueries.search_donor(first, last, 'True')

            if not self.query:
                self.donor = Donor(first.title(), last.title())
                self.dbqueries.add_donor(self.donor)
                print(f"{self.name.title()} is a new donor.")
                print(self.thank_you_message(self.name, self.donation, 0))
                self.dbqueries.add_donation(self.donor.id_num, self.donation)

            else:
                print(f"{self.name.title()} is a previous donor.\n>> ")          
                print(self.thank_you_message(self.name, self.donation, 1))
                self.dbqueries.add_donation(self.query[0], self.donation)

    def delete_donor(self):

        reply, query = self.search_for_donor()
        self.dbqueries.delete_donor(reply, query)
        

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
        self.dbqueries.get_all_donors_summary()

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

  
   
if __name__ == '__main__':
    donor_dict = {'Bob Dylan': [2000.00, 500.00, 3.00], 'Italo Calvino': [1001.00, 333.00], 'Feist Scotia': [1500.00, 30.00]}
    
    dbqueries = DBQueries(mailroom_database.dbconnection)


    for key, value in donor_dict.items():
        split_name = key.split()
        first = split_name[0]
        last = split_name[1]
        cur_donor = Donor(first, last)
        dbqueries.add_donor(cur_donor)
        for val in value:
            dbqueries.add_donation(cur_donor.id_num, val)


    dc = DonorCollection(donor_dict, dbqueries)

    main_menu(dc)


