"""
Defines the database model for donation_tracker
"""

from peewee import SqliteDatabase, Model, CharField, DateField, DecimalField, ForeignKeyField

# import peewee as pw

# database = SqliteDatabase('personjob.db')
# database.connect()
# database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        db = database


class Donor(BaseModel):
    """
        This class defines the donor table
    """
    donor_name = CharField(primary_key=True, max_length=30)


class Donation(BaseModel):
    """
        This class definies the donation tables
    """
    donor_name = ForeignKeyField(Donor, null=False)
    donation_amount = DecimalField(max_digits=7, decimal_places=2, null=False)
    donation_date = DateField(formats='YYYY-MM-DD')
