#!/usr/bin/env python3

from create_donordonation import SqliteDatabase, Donor, Donation

import logging


def populate_donors():
    """
    Add donor data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')

    donors = [
        'Stuart',
        'Cayce'
    ]

    logger.info('Creating Donor records...')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                        donor_name=donor)
                new_donor.save()

                logger.info('Database add successful')

        logger.info('Print the Donor records we saved...')

        for saved_donor in Donor:
            logger.info(f'{saved_donor.donor_name}')

    except Exception as e:
        logger.info(f'Error creating = {donor}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_donations():
    """
    Add donation data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donation class')

    DONATION_AMOUNT = 0
    DONATION_DONOR = 1

    donations = [
        (100, 'Stuart'),
        (250, 'Cayce')
    ]

    logger.info('Creating Donation records...')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for donation in donations:
            with database.transaction():
                new_donation = Donation.create(
                    donation_amount=donation[DONATION_AMOUNT],
                    donation_donor=donation[DONATION_DONOR])
                new_donation.save()

                logger.info('Database add successful')

        logger.info('Print the Donation records we saved...')

        for donation in Donation:
            logger.info('Donation amount: {}, donor name: {}'
                        .format(donation.donation_amount,
                                donation.donation_donor))

    except Exception as e:
        logger.info(f'Error creating = {donation[DONATION_AMOUNT]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_donors()
    populate_donations()
