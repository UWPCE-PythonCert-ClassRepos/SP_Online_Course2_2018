"""defines database interface for mailroom"""

from peewee import *
import datetime
import logging

# good reference on setting this at runtime
# http://timlehr.com/lazy-database-initialization-with-peewee-proxy-subclasses/
# TODO: update this to be decided at runtime
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
        self.logger = logging.getLogger(__name__)
        self.database = SqliteDatabase(database)
        for tbl in self.registered_tables:
            tbl._meta.database = self.database
        self.database.execute_sql('PRAGMA foreign_keys = ON;')
        self.database.create_tables([Donation, Donor])

    def close(self) -> None:
        self.database.close()

    def summarize_donors(self) -> dict:
        """creats summar report of donors.  Default values to 0 if no donations present.
        returns:
            dict of donors summary
                donor_name: key str of donors name
                total_donations: float of total given to date
                donation_count: int of total gifts
                average_donation: float of average amount per donation"""
        query = (Donor
                 .select(Donor.donor_name,
                 fn.sum(Donation.donation_amount_cents).alias('donation_total')
                 , fn.count(Donation.donation_amount_cents).alias('donation_count')
                 , fn.avg(Donation.donation_amount_cents).alias('average_donation')
                 )
                .join(Donation, JOIN.LEFT_OUTER)
                .group_by(Donor).dicts()
                .order_by(-fn.sum(Donation.donation_amount_cents))
                )
        results = {i['donor_name']: i for i in query}

        # normailze results to have 0s in place of None
        results_mod = {}
        try: 
            for key, value in results.items():
                inner_results = {}
                for key_, value_ in value.items():
                    if value_ is None:
                        value_ = 0
                    inner_results[key_] = value_
                results_mod[key] = inner_results
        except AttributeError:
            pass
        return results_mod

    def get_donations(self, donor:str =None) -> dict:
        """returns dict of donation objects to user
        if user provides donor, then results limited to just
        that donor
        args:
            donor: donor name from database"""
        query = (Donation
                 .select(Donation.id,
                         Donation.donation_amount_cents,
                         Donation.donation_date)
                 .where(Donation.donation_donor == donor).dicts()
                 .order_by(-Donation.donation_date)
                 )
        return {i['id']: {'id': i['id'],
                       'donation_date': i['donation_date'],
                       'donation_amount_cents': i['donation_amount_cents']} for i in query}

    def create_donation(self, donor, amount, date):
        """creates donation object"""
        return Donation.create(donation_donor=donor,
                        donation_amount=amount,
                        date=date)

    def find_donor(self, donor: str):
        """searches through donor list and returns donor
        returns none if not found.  Search is performed on donor_name.
        args:
            donor_name: donors name.
        returns:
            donor object"""

    def find_donor(self, donor_name: str):
        """searches through donor list and returns donor
        returns none if not found.  Search is performed on donor_name.
        args:
            donor_name: donors name.
        returns:
            donor object"""
        try:
            return Donor.get(Donor.donor_name == donor_name)
        except Donor.DoesNotExist:
            return None

    def create_donor(self, donor_name: str, donor_email: str = None) -> Donor:
        """creates donor in database.  Accepts donor_name and email
        then creates object.  This first checks if donor already exists and
        raises error to avoid duplication.
        args:
            donor_name: name for donor
            donor_email: contact email for donor
        returns:
            donor inctance
            """
        self.logger.info('creating new donor')
        # TODO: abstract creation of donor to Donor composition
        return Donor.create(donor_name=donor_name, donor_email=donor_email)

    def get_total_donations(self):
        """returns total donations"""
        return (Donation
                .select(fn.Sum(Donation.donation_amount)
                .alias('total_donation')))

    def get_donors(self)->set:
        """returns set of donors contained in database"""
        return set(Donor.select(Donor.donor_name))

    def update_donation(self, donation, value, field='donation_amount'):
        """update interface to update donation field in database
        args:
            donation: id for donation to update
            field: filed in donation database to update
            value: new value for update"""
        donation = Donation.get(Donation.id == donation)
        setattr(donation, field, value)
        donation.save()
        # TODO: abstract to database

    def update_donor(self, donor, value, field='email'):
        """update interface to update donor field in database.
        Defaults to email only but setup to easily expand in future.
        args:
            donor: donor name to adjust
            field: filed in donation database to update
            value: new value for update"""
        donor = Donor.get(Donor.donor_name == donor)
        setattr(donor, field, value)
        donor.save()