from mongodb_script import MailroomDB
import redis_script as rs
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Donor(object):

    #def __init__(self, name, amount_list = (500, 100, 1000, 20)):
    def __init__(self, name, zip_code):

        try:
            name.split()[1]
        except IndexError as e:
            print('The first and last name of donor must be provided\n')
            raise
        else:
            self.first_name = name.split()[0]
            self.last_name = name.split()[1] 
            self.zip_code = zip_code.split('-')[0]
            rs.set_donor_zip_code(str(self), self.zip_code)
            self.load_donation_list()    
        
    def update_amount_in_list(self, old_amount, new_amount):
        """ update first instance of old amount with new amount """

        i = 0
        while i < len(self.amount_list):
            if self.amount_list[i] == old_amount:
                self.amount_list[i] = new_amount
            i += 1

    def delete_amount_from_list(self, amount):
        """ delete first instance of amount in list """

        self.amount_list.remove(amount)

    @property
    def donation_total(self):
        return sum(int(v) for v in self.amount_list)

    @property
    def donation_count(self):
        return len(self.amount_list)

    @property
    def donation_average(self):
        return round(self.donation_total/self.donation_count,2) if self.donation_count > 0 else 0

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def save_donation(self, amount):

        mailroom = MailroomDB() 
        mailroom.add_donation(self.first_name, self.last_name, amount)

    def save_donation_list(self):
        for amount in self.amount_list:
            self.save_donation(amount)

    def load_donation_list(self):
        """ reads database and loads list """

        mailroom_db = MailroomDB()
        donation_list = mailroom_db.get_donation_list_by_donor(self.first_name, self.last_name)       
 
        self.amount_list = []
        for donation in donation_list:
             self.amount_list.append(donation['amount'])

        return self.amount_list

