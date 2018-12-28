
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donation.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database


class Donor_Collection(BaseModel):
    """
        This class defines
    """

    logger.info('Define Donation Database')
    logger.info('Specify the fields in database model, their lengths and if mandatory')

    person_name = CharField(primary_key = True, max_length = 30)
    donation_count = IntegerField()
    total_amount = FloatField(default=8)

class Donation_Amount(BaseModel):

    donation_amount = FloatField(default=8)
    from_person = ForeignKeyField(Donor_Collection, related_name='Donation Amount from Donor')

db_exist = database.table_exists('donor_collection')

database.create_tables([
    Donor_Collection,
    Donation_Amount
])

PERSON_NAME = 0
DONATION_LIST = 1

Donors = [
        ('Andrew', [1000.0]),
        ('Peter', [5000.0, 200.0]),
        ('Susan', [10000.0]),
        ('Pam', [1000.0, 3000.0, 5000.0]),
        ]
if not db_exist:
    """ initialize database with donors"""

    for item in Donors:
        with database.transaction():
            new_donor = Donor_Collection.create(
                person_name = item[PERSON_NAME],
                donation_count = len(item[DONATION_LIST]),
                total_amount = sum(item[DONATION_LIST]))

            new_donor.save()

            for amount in item[DONATION_LIST]:
                new_donation_amount = Donation_Amount.create(
                    donation_amount = amount,
                    from_person = item[PERSON_NAME])
                new_donation_amount.save()

            logger.info('Database add successful')

database.close()