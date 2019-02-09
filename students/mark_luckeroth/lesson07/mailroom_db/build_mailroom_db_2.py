"""
    Lesson 07 assignment
    Add department to personjob examples from class material
    starts with no database
"""

from mailroom_db_model_2 import *


import logging
import os
from datetime import datetime


def populate_donordata():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')

    people = [
        'Peter Pan',
        'Paul Hollywood',
        'Mary Berry',
        'Jake Turtle',
        'Raja Koduri'
        ]

    logger.info('Creating Donor records: iterate through the list of Donors')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in people:
            with database.transaction():
                new_person = Donor.create(
                        donor_name = person)
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Donor:
            logger.info(f'{saved_person.donor_name} has been saved')

    except Exception as e:
        logger.info(f'Error creating = {person}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_donationdata():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records')

    donations = {
        'Peter Pan': [10., 10., 10., 10.],
        'Paul Hollywood': [5., 5000., 5., 5.],
        'Mary Berry': [100.],
        'Jake Turtle': [123., 456., 789.],
        'Raja Koduri': [60., 60000.]
        }

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor_name, donation_list in zip(donations.keys(), donations.values()):
            for donation in donation_list:
                with database.transaction():
                    new_donation = Donation.create(
                        amount = donation,
                        donor_name = donor_name)
                    new_donation.save()

        logger.info('Reading and print all Job rows')
        for donation in Donation:
            logger.info(f'{donation.amount} was donated by {donation.donor_name}')

    except Exception as e:
        logger.info(f'Error creating =')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def pprint_db():
    """
    Print summary of database to CLI
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')
    logger.info('Printing summary of database content to CLI')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Donor
                     .select(Donor, Donation)
                     .join(Donation, JOIN.LEFT_OUTER)
                    )

        print('**********************DATA SUMMARY*************************')
        print('\n')

        for donor in query:
            try:
                print(f'Person {donor.donor_name} made a donation of {donor.donation.amount}')

            except Exception as e:
                print(f'Person {donor.donor_name} had no job')
        print('\n')
        print('********************END DATA SUMMARY***********************')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only
    database.create_tables([
        Donor,
        Donation
    ])
    database.close()

    populate_donordata()
    populate_donationdata()
    pprint_db()
