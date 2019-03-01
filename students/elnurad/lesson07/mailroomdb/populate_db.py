
import logging
from mailroom_db import *


donors = [("Bill Gates", [500, 6000]),
          ("Jeff Bezos", [10000, 400]),
          ("Hannah Smith", [40000, 60000]),
          ("John Clark", [3000, 4000]),
          ("Andrew Jones", [8000, 9000, 100])
          ]

def populate_donor():
    """
    add donors to Donor 
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    logger.info('Working with Donor class')

    logger.info('Creating Donor records: iterate through the list of tuples')
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor, donations in donors:
            with database.transaction():
                new_donor = Donor.create(
                        donor_name = donor,
                        total_donations = sum(donations),
                        donation_number = len(donations),
                        average_donation = sum(donations)/len(donations))
                new_donor.save()
                logger.info('Database add successful')

        logger.info('Print the Donor records we saved...')
        for saved_donor in Donor:
            logger.info(f'{saved_donor.donor_name} donated ${saved_donor.total_donations},'
                        f' {saved_donor.donation_number} donations and ${saved_donor.average_donation} on average')

    except Exception as e:
        logger.info(f'Error creating = {donor}')
        logger.info(e)
        

    finally:
        logger.info('database closes')
        database.close()


def populate_donation():
    """
       add each donation to Donation
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    database = SqliteDatabase('mailroom.db')




    logger.info('Working with Donation class')
   


    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor, donations in donors:
            with database.transaction():
                for donation in donations:
                    new_donation = Donation.create(
                         donation_amount = donation,
                         donor_name = donor
                        )
                new_donation.save()
                logger.info('Database add successful')

        logger.info('Print the Donation records we saved...')
        for saved_donation in Donation:
            logger.info(f'{saved_donation.donor_name} donated ${saved_donation.donation_amount}')

    except Exception as e:
        logger.info(f'Error creating ={donor}:{donation}')
        logger.info(e)
        

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    populate_donor()
    populate_donation()