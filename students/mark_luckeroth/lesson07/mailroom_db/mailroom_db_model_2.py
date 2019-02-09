"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema

"""

from peewee import *
from datetime import datetime

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')



class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor, which maintains details of someone
        that contributed a donation.
    """
    donor_name = CharField(primary_key = True, max_length = 30)
    initial_entry_date = DateTimeField(default=datetime.now)

class Donation(BaseModel):
    """
        This class defines Donation, which maintains details of the donations.
    """
    amount = DecimalField(max_digits = 10, decimal_places=2)
    donation_date = DateTimeField(default=datetime.now)
    donor_name = ForeignKeyField(Donor, null = False)

