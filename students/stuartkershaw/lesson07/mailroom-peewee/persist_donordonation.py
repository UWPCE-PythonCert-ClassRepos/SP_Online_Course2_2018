from peewee import JOIN
from create_donordonation import SqliteDatabase, Donor, Donation

import logging


def create_donor(name):
    """
        Add new donor to database
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')

    logger.info('Creating Donor record...')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        with database.transaction():
            new_donor = Donor.create(donor_name=name)
            new_donor.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {name}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def create_donation(donor, amount):
    """
        Add new donation to database
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donation class')

    logger.info('Creating Donation record...')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        with database.transaction():
            new_donation = Donation.create(
                donation_donor=donor,
                donation_amount=amount)

            new_donation.save()

            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {amount} for {donor}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def get_donor_names():
    """
        Get donor names from database
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (Donor
                 .select())

        donor_names = []

        for donor in query:
            try:
                donor_names.append(donor.donor_name)

            except Exception as e:
                logger.info(e)

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

        return donor_names


def get_donor_donations():
    """
        Get donor donations from database
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (Donation
                 .select(Donation, Donor)
                 .join(Donor, JOIN.INNER))

        donor_donations = {}

        for donation in query:
            try:
                donor_donations.setdefault(donation.donation_donor.donor_name,
                                           []).append(float(donation.donation_amount))

            except Exception as e:
                logger.info(e)

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

        return donor_donations
