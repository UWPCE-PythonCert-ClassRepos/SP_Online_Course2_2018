from peewee import *


database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor_Records(BaseModel):
    """
        This class defines Donor, which maintains details of someone
        that made a donation.
    """
    donor_name = CharField(primary_key=True, max_length=100)


class Donation_Records(BaseModel):
    """
        This class defines Donation, which maintains details of past
        donations given by Donors.
    """
    donor = ForeignKeyField(Donor_Records, backref='user_don')
    donation_amt = IntegerField()


database.create_tables([
        Donor_Records,
        Donation_Records
    ])

database.close()
