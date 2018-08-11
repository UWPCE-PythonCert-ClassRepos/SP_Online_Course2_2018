#!/usr/bin/env python3

from peewee import JOIN
from create_donordonation import SqliteDatabase, Donor, Donation

import pprint
import logging


def join_classes():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Donation
                 .select(Donation, Donor)
                 .join(Donor, JOIN.INNER))

        donations = []

        for donation in query:
            try:
                logger.info(f'{donation.donation_donor.donor_name} donated: '
                            f'{donation.donation_amount}')

                donation_info = {
                    'donor': donation.donation_donor.donor_name,
                    'amount': donation.donation_amount
                }

                donations.append(donation_info)

            except Exception as e:
                logger.info(e)

    except Exception as e:
        logger.info(e)

    finally:
        print_donations(donations)
        database.close()


def print_donations(donations):
    """
        pretty print array of donation dicts
    """
    if len(donations) > 0:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(donations)
    else:
        print('No donations to print out')


if __name__ == '__main__':
    join_classes()
