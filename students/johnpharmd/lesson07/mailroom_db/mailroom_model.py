from peewee import *


database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor instances, each of which maintains
        details of an individual donor.
    """
    title = CharField(max_length=10)
    last_name = CharField(primary_key=True, max_length=30)
    total_donation_amt = IntegerField()
    num_donations = IntegerField()


database.close()
