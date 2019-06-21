from peewee import *
import os

if not os.path.exists('donations.db'):
    db_exists = True
else:
    db_exists = False

database = SqliteDatabase('donations.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Donor_Table(BaseModel):
    full_name = CharField(max_length = 30)


class Donation_Table(BaseModel):
    donor = ForeignKeyField(Donor_Table, related_name='donated', null=False)
    donation_amt = FloatField()


database.create_tables([Donor_Table, Donation_Table])
database.close()
