"""Database setup for Mailroom"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Setting up the database')

database = SqliteDatabase('mailroom.db')

logging.info('Database {} is created'.format(database))


class BaseModel(Model):
    """
    BaseModel class to inherit from
    """
    class Meta:
        database = database


class Donor(BaseModel):
    """
    Donor Class
    """
    logger.info('Creating the Donor class')
    donor_name = CharField(primary_key=True)
    number_of_donations = IntegerField(null=True)
    donation_total = FloatField(null=True)


class Donations(BaseModel):
    """
    Donations Class
    """
    logger.info('Creating Donations class')
    donation_name = ForeignKeyField(Donor, related_name='is_donated_by')
    donation_amount = FloatField()


database.create_tables([
        Donor,
        Donations
    ])

logger.info('Created Tables')

database.close()

logger.info('Database is closed')