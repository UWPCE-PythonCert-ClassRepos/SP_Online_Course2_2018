"""This module defines the mailroom donor database model."""

import peewee as pw

db_name = 'DennisLee.db'
database = pw.SqliteDatabase(db_name)
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(pw.Model):
    """Define the base model class behind the real models."""
    class Meta:
        """Assign the database connection."""
        database = database

class Person(BaseModel):
    """
    This class defines Person, which maintains details of someone
    for whom we want to research career to date.
    """
    person_name = pw.CharField(primary_key=True, max_length=30, null=False)
    lives_in_town = pw.CharField(max_length=40, default='N/A', null=False)

class Donations(BaseModel):
    """
    This class contains records of a donor name and a donation amount.
    """
    donor_name = pw.ForeignKeyField(Person)
    donation_amount = pw.DecimalField(
        max_digits=13, decimal_places=2, auto_round=True)
    donation_date = pw.DateField(formats='YYYY-MM-DD', null=False)
    class Meta:
        """Define the primary key."""
        primary_key = pw.CompositeKey('donor_name', 'donation_date')
