import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    """
       Define BaseModel for Donor Class
    """
    class Meta:
        database = database


class Donor(BaseModel):#donor class with existing donors and their donation history
    """
       Define Donor class which maintains donor name.
    """
    donor_name = CharField(max_length = 50, unique = True)
    


class Donation(BaseModel):
    """Define Donation class which maintains donor name
    and donation amount.
    """
    donor_name = ForeignKeyField(Donor, related_name = 'donated by', null = False)
    donation_amount = FloatField()
    

database.create_tables([
        Donor,
        Donation
    ])

database.close()
