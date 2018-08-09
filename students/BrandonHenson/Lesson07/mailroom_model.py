# -*- coding: utf-8 -*-

import logging
from peewee import *
from functools import partial

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Program to build the classes from the model in the database')
logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')
logger.info('The next 3 lines of code are the only database specific code')
database = SqliteDatabase('donor.db')
logger.info('Creating a base model for peewee')


class BaseModel(Model):
    class Meta:
        database = database

logger.info('Creating a Donor class (table)')


class Donor(BaseModel):
    """This class defines a Donor"""

    username = TextField(primary_key=True)


class Donation(BaseModel):
    """This class defines a Donor"""
    value = partial(DecimalField, decimal_places=2)
    donation = value()
    user = ForeignKeyField(Donor, backref='user_don')


def create_tables():
    database.create_tables([Donor, Donation])
