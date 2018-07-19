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


def create_tabs():
    database.create_tables([Donor, Donation])