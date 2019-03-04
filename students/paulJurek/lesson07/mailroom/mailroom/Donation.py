"""donor class controlling donor behavior"""
import datetime
from peewee import IntegerField, ForeignKeyField, DateField
from peewee import Check
from . BaseModel import BaseModel
from . Donor import Donor


class Donation(BaseModel):
    donation_amount_cents = IntegerField(null=False,
                                         constraints=[Check('donation_amount_cents >= 0')])
    donation_donor = ForeignKeyField(Donor, related_name='was_filled_by',
                                     null=False)
    donation_date = DateField(null=False, default=datetime.datetime.today())

    @property
    def donation_amount(self):
        """returns donation_amount_cents in dollars"""
        return self.donation_amount_cents/100

    @donation_amount.setter
    def donation_amount(self, donation_amount):
        """converts inputs of donation amount to int and stores"""
        self.donation_amount_cents = int(donation_amount * 100)