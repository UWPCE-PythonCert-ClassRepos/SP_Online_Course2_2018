"""
    Populates the mailroom donor database
"""

from peewee import *
from ap_model import *
from datetime import date, timedelta, datetime
import random


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('maildonor.db', pragmas={'foreign_keys': 1})


def populate_donors():
    """
        Populates donors table in database
    """
    logger.info('Starting Donors table population')

    donors= ['Donor A', 'Donor B', 'Donor C', 'Donor D',
    'Donor E', 'Donor F']

    try:
        database.connect()
        for donor in donors:                        #
            if ' ' in donor:
                first, last = donor.split(' ')
            else:
                first = ''
                last = donor
            donor_s=(donor, last, first)
            with database.transaction():
                new_donor = Donors.create(
                    donor_name =donor_s[0],
                    lastname=donor_s[1],
                    firsttname=donor_s[2])
                new_donor.save()
                logger.info(f'{new_donor.donor_name} added to Donors table')

    except Exception as e:
        logger.info(f'Error creating = {donor_s[0]}')
        logger.info(e)

    finally:
        logger.info('closing database')
        database.close()

def populate_donations():
    """
       Populates donations table in database
    """
    logger.info('Starting Donations table population')
    db = [('Donor A', [3580, 34124.31, 7654]),
                     ('Donor B', [110.55, 3500]),
                     ('Donor C', [11000]),
                     ('Donor D', [2233.1, 6543.74, 4567.35]),
                     ('Donor E', [546123, 99.10, 23555, 19]),
                     ('Donor F', [78.75, 21.75])]

    donations=[(a[0],b) for a in db for b in a[1]]
    try:
        database.connect()
        for donation in donations:
            d=date.today() - timedelta(days=random.randint(1, 100))
            with database.transaction():
                new_donation = Donations.create(
                    donor_key =donation[0],
                    amount=donation[1],
                    date=d)
                new_donation.save()
                logger.info(f'{new_donation.donor_key} {new_donation.amount} '
                    +f'{new_donation.date}  added to Donations table')

    except Exception as e:
        logger.info(f'Error creating = {donation[0]} {donation[1]}, {d}')
        logger.info(e)
    finally:
        logger.info('closing database')
        database.close()


if __name__ == '__main__':
    populate_donors()
    populate_donations()
