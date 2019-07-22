"""
Name: Jared Mulholland
Assignment: Lesson 7, problem 2
Date: 7/20/2019


Make donor, and donor group class for mail room db assignment

"""

from peewee import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donor.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database
        
class DonorSummary(BaseModel):
    """
    This class defines the donor, including (based on whats in report):
    donor_name, sum_donations, count_donations and average_donations
    donor_name is hte primary key
    """
    donor_name = CharField(primary_key=True, max_length=30)
    sum_donations = DecimalField(max_digits=10, decimal_places=2)
    count_donations = IntegerField()
    average_donations = DecimalField(max_digits=10, decimal_places=2)

class Donation(BaseModel):
    """
    For table of all donations, donor_name is the foreign key
    """

    donor_name = ForeignKeyField(DonorSummary, related_name="was_donated_by", null=False)
    donation_amount = DecimalField(max_digits=10, decimal_places=2)


logger.info("creating creating tables, DonorSummary and Donation in donor_db")

database.create_tables([DonorSummary, Donation])
