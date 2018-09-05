"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
from peewee import *
from pprint import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjobdept.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


logger.info('Enable the Peewee magic! This base class does it all')


class BaseModel(Model):
    class Meta:
        database = database

logger.info('By inheritance only we keep our model (almost) technology neutral')

class Donor(BaseModel):
    """
        This class defines Donor.
    """

    donor_name = CharField(primary_key = True, max_length=40)
    donor_num = IntegerField()


class Donation(BaseModel):
    """
    This class defines a donation table
    """

    logger.info('The donation amount')
    donation_amount = DecimalField()

    logger.info('The donor')
    donor_name_two = ForeignKeyField(Donor, column_name='donor_name', null=False)


def populate_donors():
    """
		Add donor to database
	"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('donors.db')

    logger.info('Working with Donor class')

    DONOR_NAME = 0
    DONOR_NUM = 1

    donors = [('Andy', 1),('Bill', 2),('Chuck', 3),]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                    donor_name = donor[DONOR_NAME],
                    donor_num = donor[DONOR_NUM]
					)
            new_donor.save()
            logger.info('Database add successful')

        logger.info('Print the Donor records we saved...')

        for donors in Donor:
            logger.info(f'{donors.donor_name} added to database.')

    except Exception as e:
        logger.info(f'Error creating = {donor[DONOR_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


database.create_tables([Donor, Donation])

database.close()



def populate_donations():
    """
        Add donations to database
    """

    database = SqliteDatabase('donors.db')

    DONATION_AMOUNT = 0
    DONOR_NAME_TWO = 1

    donations = [
        (10.00, 'Andy'),
        (20.00, 'Andy'),
        (30.00, 'Andy'),
        (40.00, 'Bill'),
        (50.00, 'Bill'),
        (25.00, 'Chuck'),
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                new_gift = Donation.create(
                    donation_amount = donation[DONATION_AMOUNT],
                    donor_name_two = donation[DONOR_NAME_TWO])
                new_gift.save()
                logger.info('Database add successful')

            logger.info('Print the Person records we saved...')
        for donations in Donation:
            logger.info(f'{donations.gift_value} from {donations.gift_donor}')

    except Exception as e:
        logger.info(f'Error creating = {donation[GIFT_VALUE]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    populate_donors()
    populate_donations()


