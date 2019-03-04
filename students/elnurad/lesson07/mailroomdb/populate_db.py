import logging
from mailroom_db import *


donors = [("Bill Gates", [500, 6000]),
          ("Jeff Bezos", [10000, 400]),
          ("Hannah Smith", [40000, 60000]),
          ("John Clark", [3000, 4000]),
          ("Andrew Jones", [8000, 9000, 100])
          ]

def populate_database():
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
                new_donor = Donor.create(donor_name = donor)
                new_donor.save()
                logger.info(f'Database add successful: {donor}')
                for donation in donations:
                    new_donation = Donation.create(
                        donation_amount = donation,
                        donor_name = new_donor)
                    new_donation.save()
                    logger.info(f'Database add succesful:{donor} - {donation}')

        logger.info('Print the Donor records we saved')
        for saved_donor in Donor:
            logger.info(f'{saved_donor.donor_name}')


    except Exception as e:
        logger.info(f'Error creating = {donor}')
        logger.info(e)
    
    finally:
        logger.info('database closes')
        database.close()



if __name__ == '__main__':
    populate_database()
    