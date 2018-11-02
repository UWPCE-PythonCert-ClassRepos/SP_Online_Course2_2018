import logging
from peewee import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donors.db')


class BaseModel(Model):
    """
    Meta class meant for inheritance by below.
    """
    class Meta:
        database = database


class Donor(BaseModel):
    """
    Class for individual donors.
    """
    logger.info('Creating Donor class.')
    donor_name = CharField(primary_key=True)
    sum_donations = FloatField(null=True)
    number_donations = IntegerField(null=True)
    avg_donations = FloatField(null=True)


class Donation(BaseModel):
    """
    Class for individual donations.
    """
    logger.info('Creating Donation class.')
    donation_amount = FloatField()
    donor_name = ForeignKeyField(Donor, related_name='donated by')


# class Donor:
#     """Container for a single donor's data, and methods to access/manipulate that data."""
#     def __init__(self, name, donations=None):
#         self._name = name
#         if donations is None:
#             self._donations = []
#         else:
#             self._donations = donations
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self, val):
#         self._name = val
#
#     @property
#     def donations(self):
#         return self._donations
#
#     def append_donations(self, amt):
#         try:
#             self.donations.append(float(amt))
#         except ValueError:
#             print("Error: donations can only be entered as integers and floats.")
#
#     def sum_donations(self):
#         return sum(self.donations)
#
#     def number_donations(self):
#         return len(self.donations)
#
#     def avg_donations(self):
#         return self.sum_donations() / self.number_donations()
