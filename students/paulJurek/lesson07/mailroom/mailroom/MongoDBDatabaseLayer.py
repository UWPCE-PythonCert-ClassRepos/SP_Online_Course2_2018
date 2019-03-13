"""database layer for Mongo DB for mailroom exercise
Using mongoengine rather than pymongo to re-use the class
struture used before"""

import configparser
from pathlib import Path
import mongoengine
from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, IntField, ReferenceField, EmailField, DateTimeField, EmbeddedDocumentListField, EmbeddedDocumentField
import datetime
import logging


class Donation(EmbeddedDocument):
    donation_amount_cents = IntField(required=True,
                                     min_value=0)
    donation_date = DateTimeField(required=True,
                                  default=datetime.datetime.today)

    @property
    def donation_amount(self):
        """returns donation_amount_cents in dollars"""
        return self.donation_amount_cents/100

    @donation_amount.setter
    def donation_amount(self, donation_amount):
        """converts inputs of donation amount to int and stores"""
        self.donation_amount_cents = int(donation_amount * 100)


class Donor(Document):
    """donor giving to organization"""
    donor_name = StringField(required=True, max_length=55, unique=True)
    email = EmailField(required=False, max_length=55)
    donations = EmbeddedDocumentListField(Donation)


class MongoDBAccessLayer:
    """has db_init over just __init__ as some connection 
    expected to self populate __init__ (eg. sqlalchemy) so 
    this allows common interface on all layers"""

    # TODO: if set to test ensure it is torn down before start and end
    def db_init(self, run_mode: str):
        """initiates connection to sqlite database
        args: 
            database: string representing sqlite database to connect to.  
                assuming only sqlite databases."""
        self.logger = logging.getLogger(__name__)
        config = configparser.ConfigParser()
        # May need to adjust depending on where you enter.  Assuming this 
        # is entered at class dir
        config_file = Path.cwd() / 'config' / 'config_mongodb.ini'
        config.read(config_file)

        self.client = mongoengine.connect(
            db=run_mode,
            username=config.get('configuration', 'user'),
            password=config.get('configuration', 'pw'),
            host=config.get('configuration', 'connect')
        )

    def close(self) -> None:
        self.client.close()

    def summarize_donors(self) -> dict:
        """creats summar report of donors.  
        Default values to 0 if no donations present.
        returns:
            dict of donors summary
                donor_name: key str of donors name
                total_donations: float of total given to date
                donation_count: int of total gifts
                average_donation: float of average amount per donation"""
        output = {}
        for donor in Donor.objects:
            total_donations = 0
            donation_count = 0
            for donation in donor.donations:
                total_donations += donation.donation_amount_cents
                donation_count += 1
            if donation_count:
                average_donation = total_donations / donation_count
            output[donor.donor_name] = {'donor_name': donor.donor_name,
                                        'total_donations': total_donations,
                                        'donation_count': donation_count,
                                        'average_donation': average_donation}
        return output


    def get_donations(self, donor:str =None) -> dict:
        """returns dict of donation objects to user
        if user provides donor, then results limited to just
        that donor
        args:
            donor: donor name from database"""
        donor = Donor.objects.get(donor_name=donor)

        return {num: {'id': num,
                      'donation_amount_cents': donation.donation_amount_cents,
                      'donation_date': donation.donation_date} for num, donation in enumerate(donor.donations, start=1)}

    def create_donation(self, donor: str, amount: int, date: datetime=datetime.datetime.utcnow()) -> bool:
        """creates donation object.  Returns"""
        try:
            print('finding donor')
            db_donor = Donor.objects.get(donor_name=donor)
            print('donor found')
            db_donor.donations.append(Donation(donation_amount_cents=amount, donation_date=date))
            db_donor.save()
            return True
        except mongoengine.DoesNotExist:
            return False
        except:
            return False


    def find_donor(self, donor_name: str):
        """searches through donor list and returns donor
        returns none if not found.  Search is performed on donor_name.
        args:
            donor_name: donors name.
        returns:
            donor object"""
        try:
            return Donor.objects.get(donor_name = donor_name)
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
        donor = Donor(donor_name=donor_name, email=donor_email)
        donor.save()
        return donor

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

    def delete_donation(self, donation):
        """deletes donation from database.  Has
        not impact on donors"""
        # TODO: abstract to database
        donation = Donation.get(Donation.id == donation)
        donation.delete_instance()

    def delete_donor(self, donor):
        """deletes donor from database.  deletes all donations
        associated with donor as well"""
        # TODO: abstract to database
        donor = Donor.get(Donor.donor_name == donor)
        donor.delete_instance(recursive=True)

    def get_donor_details(self, donor_name):
        """returns donor details in dict give input"""
        return Donor.get(Donor.donor_name == donor_name)

    def get_donation_details(self, donation_id):
        """gets details for specific donation"""
        return Donation.get(Donation.id == donation_id)