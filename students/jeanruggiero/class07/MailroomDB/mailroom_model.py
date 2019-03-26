"""
Define database model for mailroom application.
"""

#!/usr/bin/env python

from peewee import *
import statistics

database = SqliteDatabase('mailroom.db', pragmas={'foreign_keys': 1})
database.connect()


class BaseModel(Model):
    """
    BaseModel class for mailroom database.
    """
    class Meta:
        database = database


class Donor(BaseModel):
    """
    This class defines Donor, which maintains details of all donors.
    """

    # Use person name as primary key
    name = CharField(primary_key=True, max_length=50)

    @property
    def donation_count(self):
        try:
            query = (Donation
                     .select()
                     .where(Donation.donor == self.name))
        except Exception:
            print('Error')
        return len(query)

    @property
    def donation_total(self):
        try:
            query = (Donation
                     .select()
                     .where(Donation.donor == self.name))
        except Exception:
            print('Error')
        return sum(donation.amount for donation in query)

    @property
    def donation_average(self):
        try:
            query = (Donation
                     .select()
                     .where(Donation.donor == self.name))
        except Exception:
            print('Error')
        return statistics.mean([donation.amount for donation in query])

class Donation(BaseModel):
    """
    This class defines Donation, which maintains details of all
    donations made.
    """

    # Use a generated primary key for donations since there is no
    # natural unique identifier
    amount = DecimalField(decimal_places=2, auto_round=True)
    donor = ForeignKeyField(Donor, null=False)


database.create_tables([Donor, Donation])
database.close()




