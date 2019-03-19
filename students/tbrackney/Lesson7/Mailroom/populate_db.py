"""
Populates mailroom
"""

from peewee import SqliteDatabase
from donordb_model import Donor, Donation
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
database = SqliteDatabase('donation_tracker.db')

DONOR_NAME = 0
DONATION_AMT = 1
DONATION_DATE = 2

init_donations = [
                ('Tom Selleck', 2000, '2015-01-15'),
                ('Tom Selleck', 1500, '2015-11-20'),
                ('Tom Selleck', 500, '2019-01-15'),
                ('Burt Reynolds', 45, '2017-10-01'),
                ('Nick Offerman', 1000, '2018-07-12'),
                ('Nick Offerman', 1000, '2019-03-12'),
                ('Sam Elliot', 1200, '2017-08-23'),
                ('Sam Elliot', 1200, '2019-01-23'),
                ('John Waters', 20, '2016-09-25'),
                ('John Waters', 20, '2017-09-25'),
                ('John Waters', 20, '2018-09-25'),
                ]


def create_db():
    log.debug('Creating Tables')
    database.create_tables([Donor, Donation])
    log.debug('Created Successfully')


def add_donor(donor):
    # log.debug('Updating donors')
    try:
        with database.transaction():
            new_donor = Donor.create(name=donor[DONOR_NAME])
            new_donor.save()
            log.debug('Added Donor')
    except Exception as e:
        log.debug(f'Error creating : {donor[DONOR_NAME]}')
        log.debug(e)


def add_donation(d):
    # log.debug('Updating donations')
    try:
        with database.transaction():
            new_donation = Donation.create(
                donor_name=d[DONOR_NAME],
                donation_amount=d[DONATION_AMT],
                donation_date=d[DONATION_DATE]
                )
            new_donation.save()
            log.debug('Added Donation')
    except Exception as e:
        log.debug(f'Error adding donation for : {d[DONOR_NAME]}')
        log.debug(e)


if __name__ == '__main__':
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        create_db()
        for donation in init_donations:
            add_donor(donation)
            add_donation(donation)
    except Exception as e:
        log.debug(e)
    finally:
        log.debug('Closing DB')
        database.close()
