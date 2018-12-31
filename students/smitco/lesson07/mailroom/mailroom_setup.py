# lesson 07 mailroom using peewee
# !/usr/bin/env python3

""" Set up Mailroom Donors Database Models in Peewee """

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom_db.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database

class Donor(BaseModel):
    """ This class defines the Donor, which includes Donor
        name and total, count, average of donations """
    
    logger.info('Donor entry information is gathered by query when report runs')
    
    donor_name = CharField(primary_key = True, max_length = 25)
    donor_total = DecimalField(max_digits = 12, decimal_places = 2)
    donor_count = DecimalField(max_digits = 3, decimal_places = 0)
    donor_average = DecimalField(max_digits = 9, decimal_places = 2)

class Donation(BaseModel):
    """ This class defines the Donation, which includes
        Donor name and Donation amount and a unique 
        primary key donation id using YYYYMMDD_FFLL """
    
    logger.info('Donation entry must contain all info')
    
    donation_donor = ForeignKeyField(Donor, related_name = 'was_donated_by', null = False) 
    donation_amount = DecimalField(max_digits = 9, decimal_places = 2)
    donation_date = DateField(formats = 'YYYYMMDD')
    donation_id = CharField(primary_key = True, max_length = 15)
    
    
database.create_tables([
        Donation,
        Donor
    ])

database.close()

    
    
