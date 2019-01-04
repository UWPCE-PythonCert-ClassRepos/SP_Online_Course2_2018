"""
    Mailroom using a database
    This is the schema definition
"""

from peewee import *

DATABASE = 'mail_default.db'

database = SqliteDatabase(DATABASE)
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Donor(BaseModel):
    """
        This class defines Donor, which hold details about
        individual donors.
    """
    #name of the donor
    donor_name = CharField(primary_key=True, max_length=30)
    donations = DecimalField(max_digits=10, decimal_places=2)
    
class Donation(BaseModel):
    """
    This class holds each donation made by each donor
    """
    held_by = ForeignKeyField(Donor, backref='name_person', null=False)
    dono = DecimalField(max_digits=10, decimal_places=2)
    dono_size = CharField(max_length=30)
    dono_number = IntegerField(primary_key=True)

class Details(BaseModel):
    """
        This class handles all details of donations made by each donor
    """
    name = ForeignKeyField(Donor, primary_key=True, backref='person_name', null=False)
    #number of donations made by the donor
    transactions = IntegerField()
    #average dollar amount of donations
    average = DecimalField(max_digits=10, decimal_places=2)
    #first donation made by the donor
    first_gift = DecimalField(max_digits=10, decimal_places=2)
    #most recent donation made by the donor
    last_gift = DecimalField(max_digits=10, decimal_places=2)

database.create_tables([
        Donor,
        Donation,
        Details
    ])

database.close()
