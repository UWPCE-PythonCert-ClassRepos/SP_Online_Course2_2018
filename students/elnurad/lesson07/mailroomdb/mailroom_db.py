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


class Donor(BaseModel):
    """
       Define Donor class which maintains donor name and
       donation amount. 
    """
    donor_name = CharField(primary_key = True, max_length = 50)
    total_donations = FloatField()
    donation_number = IntegerField()
    average_donation = FloatField()
    


class Donation(BaseModel):
    donation_amount = FloatField()
    donor_name = ForeignKeyField(Donor, related_name = 'donated by', null = False)





database.create_tables([
        Donor,
        Donation
    ])

database.close()
