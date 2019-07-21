"""
Name: Jared Mulholland
Assignment: Lesson 7, problem 2
Date: 7/20/2019


Populate donor_db with initial values for mail room 

"""

from peewee import *
import logging
from donor_model import *

def populate_donorsummary_table():
    """
    Add donors and donations summaries to DonorSummary table
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('donor.db')
        
    logger.info('working with donor summary table')

    DONOR_NAME = 0
    SUM_DONATIONS = 1
    COUNT_DONATIONS = 2

    donors = [
        ('Chris Cornell', 115000.00, 2),
        ('Kim Thayil', 560000.00, 2)
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            avg_don = donor[SUM_DONATIONS]/donor[COUNT_DONATIONS]

            with database.transaction():
                new_donor = DonorSummary.create(
                    donor_name = donor[DONOR_NAME],
                    sum_donations = donor[SUM_DONATIONS],
                    count_donations = donor[COUNT_DONATIONS],
                    average_donations =  avg_don)
                new_donor.save()
                logger.info('Database add successful')

        logger.info('Print the donor records we saved')
        for saved_donor in DonorSummary:
            logger.info(f'''{saved_donor.donor_name}, 
            sum donations: {saved_donor.sum_donations}, 
            count_donations: {saved_donor.count_donations},
            average_donations: {saved_donor.average_donations}''')

    except Exception as e:
        logger.info(f'Error creating = {donor[DONOR_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()  



def populate_donations_table():
    """
    Add donation instance to Donation table
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('donor.db')
        
    logger.info('working with donation table')

    DONOR_NAME = 0
    DONATION_AMOUNT = 1

    donations = [
        ('Chris Cornell', 50000.00),
        ('Chris Cornell', 65000.00),
        ('Kim Thayil', 160000.00),
        ('Kim Thayil', 400000.00)
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
 
            with database.transaction():
                new_donation = Donation.create(
                    donor_name = donation[DONOR_NAME],
                    donation_amount = donation[DONATION_AMOUNT])
                new_donation.save()
                logger.info('Database add successful')

        logger.info('Print the donor records we saved')
        for saved_donation in Donation:
            logger.info(f'{saved_donation.donor_name}, donated: {saved_donation.donation_amount}')

    except Exception as e:
        logger.info(f'Error creating = {donation[DONOR_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    populate_donorsummary_table()
    populate_donations_table()
