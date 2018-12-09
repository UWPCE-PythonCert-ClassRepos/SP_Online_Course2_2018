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
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor
    """

    logger.info('Define a donor class')

    full_name = CharField(primary_key = True, max_length = 30)
    donation_count = IntegerField()
    total_donation = DecimalField(decimal_places = 2)


class Donations(BaseModel):
    """
        This class defines Donor
    """

    logger.info('Define a donation class')
    logger.info('Uses a self generated primary key')

    full_name = ForeignKeyField(Donor, null = False)
    donation = DecimalField(decimal_places = 2)


logger.info('Initializing the tables in the database')

database.create_tables([Donor, Donations])
database.close()
