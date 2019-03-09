"""database layer for Mongo DB for mailroom exercise
Using mongoengine rather than pymongo to re-use the class
struture used before"""

"""defines database interface for mailroom"""

import configparser
from pathlib import Path
import mongoengine
from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, IntField, ReferenceField, EmailField, DatetimeField, ListField, EmbeddedDocumentField
import datetime
import logging

config = configparser.ConfigParser()
# May need to adjust depending on where you enter.  Assuming this 
# is entered at class dir
config_file = Path.cwd() / 'config' / 'config_mongodb'
config.read(config_file)
user = config["default"]["user"]
pw = config["default"]["pw"]
conn = config["default"]["connect"]


class Donation(EmbeddedDocument):
    donation_amount_cents = IntField(required=True,
                                     min_value=0)
    donation_date = DatetimeField(required=True,
                                  default=datetime.datetime.today)

    @property
    def donation_amount(self):
        """returns donation_amount_cents in dollars"""
        return self.donation_amount_cents/100

    @donation_amount.setter
    def donation_amount(self, donation_amount):
        """converts inputs of donation amount to int and stores"""
        self.donation_amount_cents = int(donation_amount * 100)


class Donor(Document):
    """donor giving to organization"""
    donor_name = StringField(required=True, max_length=55, unique=True)
    email = EmailField(required=False, max_length=55)
    donations = ListField(EmbeddedDocumentField(Donation))