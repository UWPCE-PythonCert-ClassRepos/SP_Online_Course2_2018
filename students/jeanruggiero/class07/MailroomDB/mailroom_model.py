"""
Define database model for mailroom application.
"""

#!/usr/bin/env python

from peewee import *
from playhouse.hybrid import *
import statistics

database = SqliteDatabase(None)


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
    date_added = DateField(formats='YYYY-MM-DD')

    @hybrid_property
    def donation_count(self):
        try:
            query = (Donation
                     .select()
                     .where(Donation.donor == self.name))
        except Exception:
            print('Error')
        return len(query)

    @hybrid_property
    def donation_total(self):
        query = (Donation
                 .select(fn.SUM(Donation.amount))
                 .where(Donation.donor == self.name)).scalar()
        return query

    @hybrid_property
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
    date = DateField(formats='YYYY-MM-DD')
    donor = ForeignKeyField(Donor, null=False)
