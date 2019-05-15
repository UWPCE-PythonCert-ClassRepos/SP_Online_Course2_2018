'''
Defining the MailRoom Donor schema
'''

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Donor(BaseModel):
    '''This class defines Donor, which maintains details of someone
        who has donated to date'''
    first_name = CharField(max_length = 30, null = False)
    last_name = CharField(max_length = 30, null = True)
    full_name = CharField(primary_key = True, max_length = 30)

class Donation(BaseModel):
    '''This class defines Donation, which tracks each donation given
        by donors'''
    donation = DecimalField(max_digits = 8, decimal_places = 2)
    donor_donated = ForeignKeyField(Donor, null = False)
    date_donation = DateField(formats = 'YYYY-MM-DD')

database.close()