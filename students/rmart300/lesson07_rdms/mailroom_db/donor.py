from mailroom_model import *
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Donor(object):

    def __init__(self, name, amount_list = (500, 100, 1000, 20)):

        try:
            name.split()[1]
        except IndexError as e:
            print('The first and last name of donor must be provided\n')
            raise
        else:
            self.first_name = name.split()[0]
            self.last_name = name.split()[1]
            record = Donors.select().where(Donors.first_name == self.first_name, Donors.last_name == self.last_name)
            if len(record) == 0:
                self.donor = Donors.create(first_name = self.first_name, last_name = self.last_name)
                self.amount_list = list(amount_list)
                self.save_donation_list()
            else:
                self.donor = record[0]
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

        database = SqliteDatabase('mailroom.db')
        try:

            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            new_donation = Donations.create(
                donor = self.donor,
                amount = amount,
                donation_date = datetime.now()
            )
        except Exception as ex:
            logger.error('unable to create donation {} for {} {}. exception {}'.format(str(amount), self.donor.first_name, self.donor.last_name, ex))
        finally:
            database.close()

    def save_donation_list(self):
        for amount in self.amount_list:
            self.save_donation(amount)

    def load_donation_list(self):
        """ reads database and loads list """

        donation_list = Donations.select().join(Donors).where(Donors.first_name == self.first_name, Donors.last_name == self.last_name)
        self.amount_list = []
        for donation in donation_list:
             self.amount_list.append(donation.amount)

        return self.amount_list

