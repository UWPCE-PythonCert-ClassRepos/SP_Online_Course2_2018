


import random
import logging
import decimal
from mailroom_model import *
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')


def populate_donors():
    """Populate the donor table."""

    logger.info('Populating Donor table.')

    FIRST_NAME = 0
    LAST_NAME = 1
    FULL_NAME = 2

    donor_list = [
        ('Bobby', 'Jones', 'Bobby Jones'),
        ('Willy', 'Wonka', 'Willy Wonka'),
        ('Fred', 'Hammerman', 'Fred Hammerman'),
        ('Wilma', 'Johnstone', 'Wilma Johnstone'),
        ('Bubba', 'Gump', 'Bubba Gump')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donor_list:
            logger.info('Creating Donor: ' + donor[FULL_NAME])
            with database.transaction():
                new_donor = Donors.create(
                    first_name=donor[FIRST_NAME],
                    last_name=donor[LAST_NAME],
                    full_name=donor[FULL_NAME]
                )
                new_donor.save()

        logger.info('Printing Donors:')
        for saved_donor in Donors:
            logger.info(f'{saved_donor.full_name} added to the Donors table.')

    except Exception as e:
        logger.info(f'Error creating donor: {donor[FULL_NAME]}')
        logger.info(e)

    finally:
        database.close()
        logger.info('Closing database.')


def populate_donations():
    """Populates donations table in database
     Used randomly generated dates and donations to populate this table
    """
    logger.info('Starting Donations table population')

    try:
        database.connect()
        logging.info('Connection to database successful.')
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for donor in Donors:
            # generate random donations for each donor
            for donation in range(1,10):
                logging.info(f'Generating random donation for {donor.full_name}: {donation}')
                with database.transaction():
                    new_donation = Donations.create(
                        donation_date=datetime.today() - timedelta(days=random.randint(1, 1000)),
                        donation_amount=decimal.Decimal(
                            random.randrange(1, 100000)) / 100,
                        donated_name=donor.full_name,
                    )
                    new_donation.save()
            logger.info('Database entry successful.')

        logger.info('Print the Donors records we saved...')
        for donation in Donations:
            logger.info(f'donation: {donation.donor_name} : {donation.donation_date} : {donation.donation_amount}')

    except Exception as e:
        logger.info(f'Error creating donation entry:')
        logger.info(e)

    finally:
        database.close()
        logging.info('Closed database.')


if __name__ == '__main__':
    populate_donors()
    populate_donations()

