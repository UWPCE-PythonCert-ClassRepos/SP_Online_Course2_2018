"""defines database interface for mailroom"""

from peewee import *
import datetime

database = SqliteDatabase('mailroom.db')

class BaseModel(Model):
    class Meta:
        # to be redifined by DataAccessLayer
        database = database


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


class SQLiteAccessLayer:
    """has db_init over just __init__ as some connection 
    expected to self populate __init__ (eg. sqlalchemy) so 
    this allows common interface on all layers"""

    # tables which this layer controls
    registered_tables = [Donation, Donor]

    def db_init(self, database: str):
        """initiates connection to sqlite database
        args: 
            database: string representing sqlite database to connect to.  
                assuming only sqlite databases."""
        self.database = SqliteDatabase(database)
        for tbl in self.registered_tables:
            tbl._meta.database = self.database
        self.database.execute_sql('PRAGMA foreign_keys = ON;')
        self.database.create_tables([Donation, Donor])

    def close(self):
        self.database.close()