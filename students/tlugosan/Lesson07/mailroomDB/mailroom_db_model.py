#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema

"""

from peewee import *

database = SqliteDatabase('donor_list.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor with a name and location.
    """
    person_name = CharField(primary_key=True, max_length=30, null=False)
    lives_in = CharField(max_length=50)


class Donations(BaseModel):
    """
        This class defines the Donations amount that given by a person.
        The same person can donate many times the same amount therefore
        setting a primay key as a composite of the donation_amount and
        donor_name would be less efficient

    """
    donation_amount = DecimalField(null=False, constraints=[Check('donation_amount>0')])
    donor_name = ForeignKeyField(Donor, related_name='donated_by',
                                 null=False)


database.create_tables([
    Donor,
    Donations
])

database.close()
