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
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    """This class is the base class for Peewee tables"""
    class Meta:
        "Class required for Peewee tables"""
        database = database

class Donors(BaseModel):
    """
        This class defines Donor, which maintains details of someone
        for whom donated.
    """

    logger.info('Creating Donor Class')

    donor_name = CharField(primary_key = True, max_length = 30)
    number_donation = IntegerField(null=True)
    total_donation = DecimalField(decimal_places = 2, null=True)
    ave_donation = DecimalField(decimal_places = 2, null=True)
    
class Donations(BaseModel):
    """
        This class defines Donation, which maintains details of how much was
        donated
    """

    logger.info('Creating Donation Class')

    d_name = ForeignKeyField(Donors, related_name='was_donated_by')
    d_amount = DecimalField(decimal_places = 2, null=True)

    
logger.info('Adding tables to database')
database.create_tables([Donors, Donations])
database.close()
logger.info('Database closed')
