"""defines database interface for mailroom"""

from peewee import *
import datetime


class BaseModel(Model):
    class Meta:
        # to be redifined by DataAccessLayer
        database = None


class Donor(BaseModel):
    """donor giving to organization"""
    donor_name = CharField(primary_key=True, max_length=55)
    email = CharField(max_length=55, null=True)


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


class SQLiteAccessLayer(DataAccessLayer):

    def db_init(self, database):
        """initiates connection to sqlite database"""
        BaseModel.Meta.database = database
        self.database = database
        self.database.execute_sql('PRAGMA foreign_keys = ON;')
        self.database.create_tables([Donation, Donor])
