"""
    This program populates the person, job, and department tables
"""


import logging
from create_donor_db import *


def populate_donor():
    """
    Adds donor data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    FULL_NAME = 0
    DONATION_COUNT = 1
    TOTAL_DONATION = 2

    donors = [
        ('Bom Trady', 5, 5000.00),
        ('Raron Aodgers', 2, 3500.00),
        ('Brew Drees', 3, 10500.00)
    ]

    logger.info('Creating Donor records: iterate through the list of tuples')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                        full_name = donor[FULL_NAME],
                        donation_count = donor[DONATION_COUNT],
                        total_donation = donor[TOTAL_DONATION])
                new_donor.save()
                logger.info('Database add successful')

        logger.info('Print the Donor records we saved...')
        for saved_donor in Donor:
            logger.info(f'{saved_donor.full_name} has donated {saved_donor.donation_count} times ' +\
                f' with a total donation of {saved_donor.total_donation}')

    except Exception as e:
        logger.info(f'Error creating = {donor[FULL_NAME]}')
        logger.info(e)
        logger.info('The database keeps the records clean')

    finally:
        logger.info('database closes')
        database.close()


def populate_donations():
    """
    Adds donation data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    FULL_NAME = 0
    DONATION = 1

    donations = [
        ('Bom Trady', 500.00),
        ('Bom Trady', 750.00),
        ('Bom Trady', 1000.00),
        ('Bom Trady', 1250.00),
        ('Bom Trady', 1500.00),
        ('Raron Aodgers', 1500.00),
        ('Raron Aodgers', 2000.00),
        ('Brew Drees', 2000.00),
        ('Brew Drees', 3500.00),
        ('Brew Drees', 5000.00)
    ]

    logger.info('Creating Donation records: iterate through the list of tuples')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dn in donations:
            with database.transaction():
                new_donations = Donations.create(
                        full_name = dn[FULL_NAME],
                        donation = dn[DONATION])
                new_donations.save()
                logger.info('Database add successful')

        logger.info('Print the Donation records we saved...')
        for saved_dns in Donations:
            logger.info(f'{saved_dns.full_name} made a donation of {saved_dns.donation}')

    except Exception as e:
        logger.info(f'Error creating = {dn[FULL_NAME]}')
        logger.info(e)
        logger.info('The database keeps the records clean')

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_donor()
    populate_donations()
