"""
   Assignment 2: populate the mailroom database table
"""

import logging
from create_db import *

def populate_db_donor():
    """
        populate donor class database table
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for this from a user')

    DONOR_NAME = 0
    NUM_GIFT = 1

    donors = [
        ('William Gates III', 1),
        ('Mark Zuckerberg', 1),
        ('Jeff Bezos', 1),
        ('Paul Allen', 1)]

    logger.info('Creating donor records: iterate through the list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                    donor_name = Donor[DONOR_NAME],
                    num_gift = Donor[NUM_GIFT])

                new_donor.save()
                logger.info('Database add successful')

        logger.info('Print the Donor records we saved...')

    except Exception as e:
        logger.info(f'Error creating = {Donor[DONOR_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def populate_db_make_donation():
    """
        populate make_donation class database table
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Make_Donation class')
    logger.info('Creating Donation records: just like Donor. We use the foreign key')

    DONOR_NAMES = 0
    NEW_DONATION = 1
 

    donations = [
        ('Bill Gates III', 5000),
        ('Mark Zuckerberg', 2000),
        ('Jeff Bezos', 3000),
        ('Paul Allen', 4000)]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                new_donation = Make_Donation.create(
                    donor_names = donation[DONOR_NAMES],
                    new_donation = donation[NEW_DONATION])

                new_donation.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {donation[DONOR_NAMES]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_db_donor()
    populate_db_make_donation()

