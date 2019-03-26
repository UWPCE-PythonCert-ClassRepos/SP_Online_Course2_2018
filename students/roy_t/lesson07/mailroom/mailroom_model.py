#!/usr/bin/env python3
"""
    Simple database to save donors and their donations.
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.info('Creating database: mailroom.db')
database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donors(BaseModel):
    """
    Donors table tracks the names of each donor.
    """
    logging.info('Creating Donors table.')
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    full_name = CharField(primary_key=True, max_length=100)

    class Meta:
        """Create a unique identifer for each donor."""
        index = (
            (('first_name', 'last_name'), True),
        )


class Donations(BaseModel):
    """
   Track donations from donors. A system generated key is used.
    """
    logging.info('Creating Donations table.')
    donation_date = DateField()
    donation_amount = DecimalField(decimal_places=2, null=True)
    donor_name = ForeignKeyField(Donors, related_name='by_full_name', null=False)


database.create_tables([
    Donors,
    Donations
])
logging.info('Tables created.')
database.close()
logging.info('Closing database.')