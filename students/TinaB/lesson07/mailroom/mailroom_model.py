#!/usr/bin/env python3
"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donor_database.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

logger.info('Creating the Classes from the base class')


class BaseModel(Model):
    """ Base class for peewee tables"""
    class Meta:
        database = database


class Donors(BaseModel):
    """Defines Donors
    Using a system generated key for this table
    """

    logger.info('creating donors fields')
    firstname = CharField(max_length=30)
    lastname = CharField(max_length=30)
    fullname = CharField(primary_key=True, max_length=30)
    #total_donation = DecimalField(decimal_places=2, null=True)
    #average_donation = DecimalField(decimal_places=2, null=True)

    logger.info('creating donors class')

    class Meta:
        """creating our unique identifier for this table"""
        indexes = (
            # create a unique index on firstname and lastname
            (('firstname', 'lastname'), True),  # Note the trailing comma!!!!!!
            )


class Donations(BaseModel):
    """Defines donations from donors
    Using a system generated key for this table
    """
    logger.info('creating donation fields')
    donation_date = DateField()
    donation_amount = DecimalField(decimal_places=2, null=True)
    #donated_by = ForeignKeyField(Donors, related_name='by_donor', null=False)
    donated_by = ForeignKeyField(Donors, related_name='by_fullname', null=False)

    logger.info('creating donation class')
