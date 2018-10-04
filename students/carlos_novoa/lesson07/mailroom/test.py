"""
Used for testing PeeWee and mailroom
"""

import logging
from models import *  # noqa F403

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('mailroom.db')  # noqa F403


def add_people():

    FIRST_NAME = 0
    LAST_NAME = 1

    donors = [
        ('Jim', 'Halpert'),
        ('Pam', 'Beesley'),
        ('Dwight', 'Shrute'),
        ('Michael', 'Scott'),
        ('Andy', 'Bernard')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                n = Donor.create(  # noqa F403
                        first_name=donor[FIRST_NAME],
                        last_name=donor[LAST_NAME])
                n.save()

        logger.info('People added.')

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def add_donations():

    DONATION_AMT = 0
    LAST_NAME = 1

    donations = [
        (1.0, 'Halpert'),
        (1000.0, 'Beesley'),
        (2000.0, 'Beesley'),
        (3000.0, 'Beesley'),
        (2.0, 'Shrute'),
        (3.0, 'Shrute'),
        (10.0, 'Scott'),
        (20.0, 'Scott'),
        (30.0, 'Scott'),
        (10.0, 'Bernard'),
        (20.0, 'Bernard'),
        (30.0, 'Bernard')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                n = Donation.create(  # noqa F403
                        donation=donation[DONATION_AMT],
                        donor=donation[LAST_NAME])
                n.save()

        logger.info('Donations added.')

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def query_donors():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Donor  # noqa F403
                 .select(Donor, Donation)  # noqa F403
                 .join(Donation, JOIN.INNER))  # noqa F403

        for row in query:
            logger.info(f'{row.last_name} {row.donation.donation}')
    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def check_donor(key):
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (Donor  # noqa F403
                .select(Donor, Donation)  # noqa F403
                .join(Donation, JOIN.INNER)  # noqa F403
                .where(Donor.last_name == key))  # noqa F403

        if query.exists():
            return True

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    add_people()
    add_donations()
    # query_donors()
    # check_donor('Halpert')
