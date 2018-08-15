import os,re
from donor import Donor
from functools import reduce
from mongodb_script import MailroomDB 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DonorCollection(object):

    letter_directory = 'temp/'

    def __init__(self, donors=()):
        """ initialize donor_collection """

        self.donor_list = []

    def validate_and_create_thank_you(self, name, amount):
        """ send a thank you email to the donor for donation """

        try:
            amount = float(amount)
        except ValueError as e: 
            return 'invalid donation amount: ' + str(amount)

        existing_donor = None
        for d in self.donor_list:
            if name == str(d):
                existing_donor = d
                break

        if existing_donor is not None:
            existing_donor.amount_list.append(amount)
            existing_donor.save_donation(amount)
        else:
            try:
                d = Donor(name,[amount])
            except IndexError as e:
                return 'Could not send thank you.  The first and last name of donor must be provided\n'
            else:
                self.donor_list.append(d)
        return f"Hi {d}\nThank you for your donation of {amount} to the mailroom!\n"

    def send_thank_you(self):
        """
            prompt user for name and donation amount, add to donation dictionary
            provide list of names if user enters \'list\' as name
        """

        name = 'list'
        while name == 'list':
            name = input("Provide full name: ").strip()
            if name == 'list':
                for donor in self.donor_list:
                    print(donor)

        amount = input("Provide a donation amount:")
        thank_you_message = self.validate_and_create_thank_you(name, amount)
        print(thank_you_message)

    def create_report(self):
        """ Print a list of donors, sorted by total historical donation amount"""

        title = "{0:20} | {1:15} | {2:10} | {3:15}".format('Donor Name','Total Given','Num Gifts','Average Gift')
        print(title)

        #sort the dictionary by descending order of the sum of values
        sorted_list = sorted(self.donor_list, key=lambda d: d.donation_total, reverse=True)
        for donor in sorted_list:
            data_row = "{0:20}  ${1:>15}   {2:>10}   ${3:>15}".format(str(donor),
                str(donor.donation_total), str(donor.donation_count), str(donor.donation_average))
            print(data_row)

    def display_all_donations(self):

        database = SqliteDatabase('mailroom.db')
        try:

            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            print("{0:10}  {1:>25}   ${2:>8}".format('Id','Donor Name','Donation Amount'))

            for donation in Donations:
                row = "{0:10}  {1:>25}   ${2:>8}".format(donation.id, 
                       f'{donation.donor.first_name} {donation.donor.last_name}', str(donation.amount))
                print(row)
        except Exception as ex:
            logging.error('unable to load data for {}. Exception: {}'.format(donation, ex))
        finally:
            database.close()

    def update_donation(self):

        self.display_all_donations()
        donation_id = input("Please provide id of donation to update: ")
        
        database = SqliteDatabase('mailroom.db')
        try:

            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            donation = Donations.get(Donations.id == int(donation_id))
            old_amount = donation.amount
            amount = input(f"Current amount is ${old_amount}. What amount would you like to save? ")
            donation.amount = float(amount)
            donation.save()
            
            for donor in self.donor_list:
                if donor.first_name == donation.donor.first_name and donor.last_name == donation.donor.last_name:
                     donor.update_amount_in_list(old_amount, donation.amount)
                     break

        except Exception as ex:
            logging.error('unable to update data for {}. Exception: {}'.format(donation, ex))
        finally:
            database.close()

    def delete_donation(self):

        self.display_all_donations()
        donation_id = input("Please provide id of donation to delete: ")

        database = SqliteDatabase('mailroom.db')
        try:

            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')

            donation = Donations.get(Donations.id == int(donation_id))
            amount = donation.amount
            donation.delete_instance()

            for donor in self.donor_list:
                if donor.first_name == donation.donor.first_name and donor.last_name == donation.donor.last_name:
                    donor.delete_amount_from_list(amount)
                    break

        except Exception as ex:
            logging.error('unable to update data for {}. Exception: {}'.format(donation, ex))
        finally:
            database.close()


    def write_letters(self):
        """ write letters to every donor in dict """

        #clear files from directory before creating new ones
        for f in os.listdir(DonorCollection.letter_directory):
            if '.txt' in f:
                os.remove(DonorCollection.letter_directory + f)

        for donor in self.donor_list:
            donation_num = 1
            for donation_amt in donor.amount_list:
                message = f"Dear {donor.first_name} {donor.last_name},\n\n    \
                            Thank you for your very kind donation of ${donation_amt}.\n\n    \
                            It will be put to very good use.\n\n    Sincerely,\n \
                                    -The Team"
                with open(f"{DonorCollection.letter_directory}{donor.first_name}_{donor.last_name}_{donation_num}.txt",'w') as f:
                    f.write(message)
                donation_num += 1

    @staticmethod
    def challenge(x,factor):
        return x*factor
    
    def greater_than_min_value(self, x):
        return x >= self.min_value

    def less_than_max_value(self, x):
        return x <= self.max_value

    def donation_challenge(self):
        question = "By what factor would you like to increase the donations? "
        my_factor = int(input(question))
        question = "What is the minimum allowed amount? "
        self.min_value = int(input(question)) if question is not None else 0
        question = "What is the maximum allowed amount? "
        self.max_value = int(input(question)) if question is not None else 0
        

        for donor in self.donor_list:
            amount_list = donor.amount_list[:]
            amount_list = list(filter(self.greater_than_min_value, amount_list))
            amount_list = list(filter(self.less_than_max_value, amount_list))

            factor_list = [my_factor]*len(amount_list)
            challenge_list = list(map(DonorCollection.challenge, amount_list, factor_list))
            amount_list = challenge_list[:]
            challenge_sum = reduce(lambda x,y: x+y, amount_list)
            print(f"If you limited the donations between {self.min_value} and {self.max_value}")
            print(f"and increased by a factor of {my_factor}, then the total donation for {donor} would be {challenge_sum}!")

        
    def load_donor_collection(self):
        """ function to load donor collection from existing records in database """

        mailroom = MailroomDB()
        donor_list_from_db = mailroom.get_donor_list()
        for existing_donor in donor_list_from_db:
            donor = Donor(f"{existing_donor['first_name']} {existing_donor['last_name']}")
            self.donor_list.append(donor)
            donor.load_donation_list()
