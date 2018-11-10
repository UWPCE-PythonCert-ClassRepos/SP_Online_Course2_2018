"""
    Populates the mailroom donor database

"""

from mailroom_model import *
from datetime import datetime, timedelta
import random
import decimal

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donor_database.db')


def populate_donors():
    """Populates donors table in database"""
    logger.info('Starting Donors table population')

    FIRST_NAME = 0
    LAST_NAME = 1
    FULLNAME = 2

    donors = [
        ("William", "Gates", "William Gates"),
        ("Mark", "Zuckerberg", "Mark Zuckerberg"),
        ("Jeff", "Bezos", "Jeff Bezos"),
        ("Paul", "Allen", "Paul Allen"),
        ("Steven", "Hawking", "Steven Hawking"),
        ("Justin", "Timberlake", "Justin Timberlake")
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donors.create(
                    firstname=donor[FIRST_NAME],
                    lastname=donor[LAST_NAME],
                    fullname=donor[FULLNAME]
                )
                new_donor.save()
                logger.info('Database add successful')

        logger.info('Print the Donors records we saved...')
        for saved_donor in Donors:
            logger.info(f'{saved_donor.fullname} fullname added to Donors table')
            logger.info(f'{saved_donor.firstname} {saved_donor.lastname} first and last added to Donors table')

    except Exception as e:
        logger.info(f'Error creating = {donor[FIRST_NAME]} {donor[LAST_NAME]} - {donor[FULLNAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('closing database')
        database.close()


def populate_donations():
    """Populates donations table in database
     Used randomly generated dates and donations to populate this table

    """
    logger.info('Starting Donations table population')

    DONATION_DATE = 0
    DONATION_AMOUNT = 1
    DONATED_BY = 2

    d = datetime.today() - timedelta(days=random.randint(1, 301))

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for donor in Donors:
            # Randomly generated number of donations
            #donation_times = random.randint(1, 10)
            for donation in range(random.randint(1, 10)):
                with database.transaction():
                    # random date in last year
                    # random donation amount converted to decimal
                    # pulling donor fullname as id
                    new_donation = Donations.create(
                        donation_date=datetime.today() - timedelta(days=random.randint(1, 301)),
                        donation_amount=decimal.Decimal(
                            random.randrange(1, 9999999))/100,
                        donated_by=donor.fullname,
                    )
                    new_donation.save()
            logger.info('Database add successful')

        logger.info('Print the Donors records we saved...')
        for don in Donations:
            logger.info(f'donation: {don.id} : {don.donation_date} : {don.donation_amount} : '
                        + f' donor_id: {don.donated_by} has been added to the Donations table ')
    except Exception as e:
        logger.info(f'Error creating = {donation[DONATION_DATE]} {donation[DONATION_AMOUNT]}'
                    + f'{donation[DONATED_BY]}')
        logger.info(e)
        logger.info('See how the database protects our data')
    finally:
        logger.info('closing database')
        database.close()


if __name__ == '__main__':
    populate_donors()
    populate_donations()
