# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 11:21:03 2018

@author: HP-Home
"""

import logging
from peewee import *
from functools import partial

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('donor.db')
#database.connect()
#database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

logger.info('Creating a base model for peewee')
class BaseModel(Model):
    class Meta:
        database = database

logger.info('Creating a Donor class (table)')

class Donor(BaseModel):
    """
        This class defines a Donor, which maintains details of someone
        for whom we want track.
    """
    
    username = TextField(primary_key=True)
    #donation = DecimalField(decimal_places=2)
    
class Donation(BaseModel):
    """
        This class defines a Donor, which maintains details of someone
        for whom we want track.
    """
    value = partial(DecimalField, decimal_places=2)
    donation = value()
    user = ForeignKeyField(Donor, backref='user_don')


#logger.info('Creating Donor table')
#database.create_tables([Donor])
#logger.info('Closing databse')
#database.close()
    
def populate_db():
    
    """
    add donor data to database
    """
    database.create_tables([Donor, Donation])
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    #database = SqliteDatabase('donor.db')

    logger.info('Working with Person class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for this from a user')

#    NAME = 0
#    DONATION = 1
#    
    donors = [('Karl', [100, 200, 300.55]),
        ('Bob', [400, 500, 600]),
        ('Woody', [700, 800, 900]),
        ('Mary', [455.99])]
    
    logger.info('Creating Donor records: iterate through the list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')
    
    for users, donations in donors:
        user = Donor.create(username=users)
        for donation in donations:
            Donation.create(user=user, donation=float(donation))
    
#    try:
#        database.connect()
#        database.execute_sql('PRAGMA foreign_keys = ON;')
#        for donor, donations in donors:
#            for money in donations:
#                with database.transaction():
#                    new_donor = Donor.create(
#                            name = donor,
#                            donation = money)
#                        
#                    new_donor.save()
#                    logger.info('Database add successful')
#
#        logger.info('Print the Person records we saved...')
#        for saved_donor in Donor:
#            logger.info(f'{saved_donor.name} made a donation of ${saved_donor.donation}')
#
#    except Exception as e:
#        logger.info(f'Error creating = {donor[NAME]}')
#        logger.info(e)
#        logger.info('See how the database protects our data')
#
#    finally:
#        logger.info('database closes')
#        database.close()
        
if __name__ == '__main__':
    populate_db()