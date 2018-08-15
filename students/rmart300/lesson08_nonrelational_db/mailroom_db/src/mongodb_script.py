"""
    class handling creation, interaction with, and deltion of mailroom 
    mongodb database
"""

import pprint
import login_database
import utilities
from bson.objectid import ObjectId

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

class MailroomDB:

    def __init__(self, refresh_db=False):
        self.db = client['mailroom']
        self.donations = self.db['donations']

        if refresh_db:
            self.db.drop_collection('donations')
            self.initiate_database()

    def initiate_database(self):

        donation_list = []

        FIRST_NAME = 0
        LAST_NAME = 1

        donors = [
                  ('Fred', 'Smith'),
                  ('Terrie','Ann'),
                  ('Murray', 'Martin'),
                  ('Josh', 'Jones'),
                  ('Jane', 'Doe')
                 ]

        donations = [ 500, 1000, 200, 20 ]

        for donor in donors:

            for donation in donations:

                new_donor_dict = { 'first_name': donor[FIRST_NAME],
                                   'last_name': donor[LAST_NAME],
                                   'amount': int(donation),
                                   'donation_date': datetime.now(),
                                 }

                donation_list.append(new_donor_dict)

        with login_database.login_mongodb_cloud() as client:

            try:
                self.donations.insert_many(donation_list)
                log.info("successfully loaded mongodb with donation data")
            except Exception as ex:
                log.info("failed to load mongodb with donation data: {ex}")


    def get_donor_list(self):

        return self.donations.distinct('first_name','last_name')

    def get_donation(self, donation_id):
    
        return self.donations.find_one({'_id': ObjectId(donation_id)})

    def update_donation(self, donation_id, amount):    
    
        doc = get_donation(donation_id)
        doc['amount'] = amount        

        self.donations.update({"_id": ObjectId(donation_id)}, doc, upsert=True) 

    def delete_donation(self, donation_id):
    
        self.donations.remove({'id': donation_id})
    
    def show_donations_by_donor(self, first_name, last_name):
    
        cursor = self.donations.find( {'$and': [{'first_name': {'$eq': first_name}}, {'last_name': {'$eq': last_name}}]}).sort('donation_date', 1)
    
        for doc in cursor:
            print(f"Donor: {doc['first_name']} {doc['last_name']} Amount: {doc['amount']} Date: {doc['donation_date']}")
    
    def show_donations(self):

        for doc in self.donations:
            print(f"_id: {doc['_id']} Donor: {doc['first_name']} {doc['last_name']} Amount: {doc['amount']} Date: {doc['donation_date']}")

