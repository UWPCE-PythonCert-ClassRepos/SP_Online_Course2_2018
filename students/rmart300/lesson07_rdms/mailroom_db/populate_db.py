"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from mailroom_model import *
from datetime import datetime

def populate_donor_table():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Person class')

    FIRST_NAME = 0
    LAST_NAME = 1

    donors = [
        ('Fred', 'Smith'),
        ('Terrie','Ann'),
        ('Murray', 'Martin'),
        ('Josh', 'Jones'),
        ('Jane', 'Doe')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                    first_name = donor[FIRST_NAME],
                    last_name = donor[LAST_NAME]
                    )
                new_donor.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {donor[FIRST_NAME]} {donor[LAST_NAME]}')
        logger.info(e)

    finally:
        database.close()

def populate_donation_table():
    """
        add donations to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with donation class')

    AMOUNT = 0
    DONATION_DATE = 1
    DONOR = 2

    donations = [ 500, 1000, 200, 20 ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            for donor in Donor:
                with database.transaction():
                    new_donation = Donation.create(
                        amount = int(donation),
                        donation_date = datetime.now(),
                        donor = donor.id
                        )
                    new_donation.save()
                    logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {donation} for {donor.first_name} {donor.last_name}')
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    populate_donor_table()

    populate_donation_table()

