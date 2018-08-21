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


def update_donor(old_name, new_name):
    """
    Update donor name
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')

    logger.info('Updating Donor record...')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        with database.transaction():
            update_donor_name = Donor.update(donor_name=new_name)\
                .where(Donor.donor_name == old_name)

            update_donor_donations = Donation.update(donation_donor=new_name)\
                .where(Donation.donation_donor == old_name)

            update_donor_name.execute()
            update_donor_donations.execute()

            logger.info('Database update successful')

    except Exception as e:
        logger.info(f'Error updating {old_name} to {new_name}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def delete_donor(name):
    """
    Delete donor
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')

    logger.info('Deleting Donor record...')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        with database.transaction():
            donor = Donor.get(donor_name=name)

            delete_donor_donations = Donation.delete()\
                .where(Donation.donation_donor == name)

            donor.delete_instance()
            delete_donor_donations.execute()

            logger.info('Database delete successful')

    except Exception as e:
        logger.info(f'Error deleting {name}')
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


def update_donation(donor, donation):
    print('Updating donation {} for {}...'.format(donor, donation))


def delete_donation(donor, donation):
    print('Deleting donation {} for {}...'.format(donor, donation))


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
                donor_donations\
                    .setdefault(donation.donation_donor.donor_name,
                                []).append(float(donation.donation_amount))

            except Exception as e:
                logger.info(e)

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

        return donor_donations
