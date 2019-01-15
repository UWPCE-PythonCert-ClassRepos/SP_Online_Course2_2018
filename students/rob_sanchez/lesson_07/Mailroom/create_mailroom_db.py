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

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Donors(BaseModel):
    """
        This class defines Donor, which maintains the records
        for our current donors.
        Using generated keys to assign a unique identifier for
        each donor.
    """

    donor_name = CharField(unique=True, max_length=30)


class Donations(BaseModel):
    """
        This class defines Donations from our current donors.
        Using generated keys because each donor can have multiple donations.
    """

    donor = ForeignKeyField(Donors, null=False)
    donation = DecimalField(max_digits=7, decimal_places=2)


logger.info(' Creating Mailroom database...')
database.create_tables([
        Donors,
        Donations
    ])
logger.info(' Done...')
database.close()
