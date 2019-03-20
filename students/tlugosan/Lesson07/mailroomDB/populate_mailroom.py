"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from mailroom_db_model import *

import logging


def populate_donor_db():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('donor_list.db')

    logger.info('Working with Person class')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1

    donors = [
        ('Toni Orlando', 'Sumner'),
        ('Amanda Clark', 'Seattle'),
        ('Robin Hood', 'NeverLand'),
        ('Gina Travis', 'Coventry'),
        ('Mark Johnson', 'Colchester')
    ]

    logger.info('Creating Donor records: iterate through the list of tuples')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in donors:
            with database.transaction():
                new_person = Donor.create(
                    person_name=person[PERSON_NAME],
                    lives_in=person[LIVES_IN_TOWN])
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Donor:
            logger.info(
                f'{saved_person.person_name} lives in {saved_person.lives_in}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)

    finally:
        database.close()


def populate_donations_db():
    """
        add donations amount to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('donor_list.db')

    logger.info('Migrating initial data into tables.')

    DONOR_NAME = 0
    DONATION_AMOUNT = 1

    donations_list = [
        ('Toni Orlando', 150.00),
        ('Toni Orlando', 200.00),
        ('Toni Orlando', 100.00),
        ('Amanda Clark', 1800.00),
        ('Robin Hood', 1234.56),
        ('Robin Hood', 4500.34),
        ('Robin Hood', 765.28),
        ('Gina Travis', 75.00),
        ('Mark Johnson', 850.00),
        ('Mark Johnson', 20.14),
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations_list:
            with database.transaction():
                new_donation = Donations.create(
                    donor_name=donation[DONOR_NAME],
                    donation_amount=donation[DONATION_AMOUNT])
                new_donation.save()

        logger.info('Reading and print all Departments rows')
        for donation in Donations:
            logger.info(f'{donation.donor_name} donated '
                        f'${donation.donation_amount}')

    except Exception as e:
        logger.info(f'Error creating = {donation[DONOR_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_donor_db()
    populate_donations_db()
