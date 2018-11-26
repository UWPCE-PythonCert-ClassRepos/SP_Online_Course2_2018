#!/usr/bin/env python3

from peewee import *

database = SqliteDatabase('donors.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database

class IndividualDonor(BaseModel):
    """
    An individual donor table, consisting of a name, set of columns for commonly used attributes
    including total donations and average donation
    """
    name = CharField(primary_key = True, max_length = 30, unique = True, null = False)
    total_donations = FloatField()
    average_donation = FloatField()

class Donation(BaseModel):
    """
    A donation table, consists of the amount and foreign key for the donor
    """
    amount = FloatField()
    donor = ForeignKeyField(IndividualDonor, related_name='was donated by', null = False)

exists = database.table_exists('donation')

database.create_tables([
        IndividualDonor,
        Donation
    ])

def create_initial_data(populate):
    """ Create initial database dataset """
    # define a starting set of donors
    donors_array = [
    ("Bill Ted", [353.53, 348.1, 25.00]),
    ("Frank Fred", [120.50, 56.76, 1.50]),
    ("Laura Todd", [5.75]),
    ("Steve Lincoln", [75.38, 89.9]),
    ("Lisa Grant", [175.50, 34.20])
    ]

    # populate our database if this is the first time we've run
    if populate:
        for donor in donors_array:
            with database.transaction():
                total_donations = sum(donor[1])
                avg_donation = total_donations / len(donor[1])
                new_donor = IndividualDonor.create(name = donor[0], total_donations = total_donations, average_donation = avg_donation)
                new_donor.save()
                for donation in donor[1]:
                    new_donation = Donation.create(donor = donor[0], amount = donation)
                    new_donation.save()

def reset_data():
    """ Reset the intial database state, useful for tesing """
    Donation.delete().execute()
    IndividualDonor.delete().execute()
    create_initial_data(True)

create_initial_data(not exists)

database.close()

