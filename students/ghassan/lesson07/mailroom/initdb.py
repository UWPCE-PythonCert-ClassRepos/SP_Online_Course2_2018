from mailroom_db import *
import logging
from db_ops import update_donations


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_donors():
    """
    Populating the mailroom (donors) db
    :return:
    """

    database = SqliteDatabase('mailroom.db')
    logger.info('Databse {} is initialized'.format(database))

    donors = [
        'Jack Black',
        'James Ford',
        'Edward edwardson',
        'Ron Swanson',
        'Robert Robertson',
        'Alexander Alexanderson'
    ]

    logger.info('Creating donors records')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                    donor_name=donor
                )
                logger.info('Donor {} was added to db'.format(donor))
    except Exception as ex:
        logger.error('Unable to create a record for {}. Err: {}'.format(donor, ex))
    finally:
        database.close()


def populate_donations():
    """
    Popluating donations
    :return:
    """
    database = SqliteDatabase('mailroom.db')
    logger.info('Databse {} is initialized'.format(database))

    DONOR_NAME = 0
    DONATION_AMOUNT = 1

    donations = [
        ('Jack Black', 55.44),
        ('Jack Black', 100.22),
        ('Jack Black', 300.00),
        ('Edward edwardson', 11.11),
        ('Ron Swanson', 199.55),
        ('Alexander Alexanderson', 299.00)
    ]

    logger.info('Creating donors records')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                new_donation = Donations.create(
                    d_name=donation[DONOR_NAME],
                    donation_amount=donation[DONATION_AMOUNT]
                )
                logger.info('Donation {} for donor: {} was added to db'.format(
                    donation[DONATION_AMOUNT], donation[DONOR_NAME]))
    except Exception as ex:
        logger.error('Unable to create a record for {}. Err: {}'.format(donation, ex))
    finally:
        database.close()


if __name__ == '__main__':
    populate_donors()
    populate_donations()
    update_donations()
