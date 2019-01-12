#!/usr/bin/env python3

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from create_mailroom_db import *
import pprint
from datetime import datetime


def populate_donors():
    """
        Adds initial Donor data to the database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with the Donor class')

    DONOR_NAME = 0

    donors = [
        ('Tom Cruise'), ('Michael Jordan'), ('Katy Perry'), ('Adam Sandler')]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info('Adding new donors...')
        for donor in donors:
            with database.transaction():
                new_donor = Donors.create(donor_name=donor)
                new_donor.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.error(f'Error creating = {donor}')
        logger.error(e)

    finally:
        logger.info('closing database...')
        database.close()


def populate_donations():
    """
        Adds initial Donor data to the database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with the Donations class')

    DONOR_NAME = 0
    DONATION = 1

    donors = [
        (1, 100),
        (1, 200),
        (1, 300),
        (2, 1300),
        (3, 4500),
        (3, 1500),
        (4, 500),
        (4, 2400),
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info('Adding new donations...')
        for donor in donors:
            with database.transaction():
                donations = Donations.create(
                    donor=donor[DONOR_NAME],
                    donation=donor[DONATION])
                donations.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.error(f'Error creating = {donor[DONOR_NAME]}')
        logger.error(e)

    finally:
        logger.info('closing database...')
        database.close()


def select_donors():
    """
        Produces a list using pretty print that shows all of
        the departments a person worked in for every job they ever had.
    """
    database = SqliteDatabase('mailroom.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        names_query = (Donors
                       .select(Donors.donor_name,
                               fn.SUM(Donations.donation).alias('total'),
                               fn.COUNT(Donations.donation).alias('num'),
                               fn.AVG(Donations.donation).alias('avg'))
                       .join(Donations, on=(Donors.id == Donations.donor_id))
                       .group_by(Donors.donor_name)
                       .order_by(fn.AVG(Donations.donation).desc())
                       .namedtuples()
                       )

        for name in names_query:
            print("\nDonor name: {}".format(str(name.donor_name)))
            print("Total Given: ${}".format(str(name.total)))
            print("Num Given: {}".format(str(name.num)))
            print("Average: {}".format(str(name.avg)))

    except Exception as e:
        logger.error(e)

    finally:
        database.close()


def day_diff(d1, d2):
    date1 = datetime.strptime(d1, '%Y-%m-%d')
    date2 = datetime.strptime(d2, '%Y-%m-%d')
    return abs((date2 - date1).days)


if __name__ == '__main__':
    # populate_donors()
    # populate_donations()
    select_donors()
