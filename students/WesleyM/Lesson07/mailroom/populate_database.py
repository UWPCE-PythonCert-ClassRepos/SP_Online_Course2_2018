"""
    Populates Donor Database
"""

from create_database import *
from operations_database import update_donations

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_donors():
    """
    add donor data to database
    """

    database = SqliteDatabase('donor_database.db')

    logger.info('Working with Donor class')

    DONOR_NAME = 0
    DONATION_TOTAL = 1
    DONATION_AVERAGE = 2
    DONATION_NUMBER = 3

    donors = [
        'Alice Adams Ron',
        'Bob Be-Lake',
        'Charles Cruz',
        'Denise Dnice',
        'Edward Eduardo'
        ]

    logger.info('Creating Donor records:')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donors.create(donor_name = donor)
                logger.info('Donor {} was added to the database'.format(donor))

    except Exception as e:
        logger.info('Error creating = {}'.format(donor))
        logger.info(e)

    finally:
        logger.info('Database closes')
        database.close()

def populate_donations():
    """
    add donations data to database
    """

    database = SqliteDatabase('donor_database.db')

    logger.info('Working with Donation class')

    DONOR_NAME = 0
    DONOR_DONATION = 1

    donations = [
        ('Alice Adams Ron', 20),
        ('Bob Be-Lake', 100),
        ('Charles Cruz', 30),
        ('Denise Dnice', 10),
        ('Edward Eduardo', 25)
        ]

    logger.info('Creating Donation records:')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                new_donation = Donations.create(
                    d_name = donation[DONOR_NAME],
                    d_amount = donation[DONOR_DONATION])
                new_donation.save()
            logger.info('Donor {} donated ${}'.format(donation[DONOR_NAME],
                                                      donation[DONOR_DONATION]))

    except Exception as e:
        logger.info(f'Error creating = {donation[DONOR_NAME]}')
        logger.info(e)

    finally:
        logger.info('Database closes')
        database.close()


if __name__ == '__main__':
    populate_donors()
    populate_donations()
    update_donations()
