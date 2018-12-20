"""
    Assignment 2: Create the Mailroom database
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_key = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor, which maintains details of someone
        for whom we want to dononate.
    """

    logger.info('Note how we defined the Donor class')
    logger.info('Specify the fields in our model...')

    donor_name = CharField(primary_key = True, max_length = 30)
    num_gift = IntegerField(null=True)
    total_amount = FloatField(default=8) # Following Cindy's code


class Make_Donation(BaseModel):
    """
        This class defines Donations, which maintains details of donnations
        made by Donors
    """

    logger.info('Note how we defined the Make_Donations class')
    donor_names = ForeignKeyField(Donor, null = False) # related_name?
    new_donation = FloatField(default=8)



logger.info('Create the table format')
database.create_tables([
        Donor,
        Make_Donation])


db_exist = database.table_exists('donor')

DONOR_NAME = 0
DONATION = 1

Donors = [
        ('William Gates III', [200, 500]),
        ('Mark Zuckerberg', [2000, 3000]),
        ('Jeff Bezos', [4000, 5000]),
        ('Paul Allen', [100, 150]),
        ]
if not db_exist:
    """ initialize database with donors"""

    for item in Donors:
        with database.transaction():
            new_donor = Donor.create(
                donor_name = item[PERSON_NAME],
                num_gift = len(item[DONATION]),
                total_amount = sum(item[DONATION]))

            new_donor.save()

            for amount in item[DONATION]:
                new_donations = Make_Donation.create(
                    new_donation = amount,
                    donor_names = item[DONOR_NAME])
                new_donations.save()

logger.info('Database add successful')

logger.info('Databased closed')
database.close()
