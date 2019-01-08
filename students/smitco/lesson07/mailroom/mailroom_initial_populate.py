# lesson 07 mailroom using peewee
# !/usr/bin/env python3

""" Set up Donor Database Models in Peewee"""

import logging
from mailroom_setup import *


logger = logging.getLogger(__name__)
database = SqliteDatabase('mailroom_db.db')

def populate_initial_donors():
    """ Populate initial donor data """
    
    
    DONOR_NAME = 0
    DONOR_TOTAL = 1
    DONOR_COUNT = 2
    DONOR_AVERAGE = 3
    
    donors = [
        ('John Travolta', 12500, 2, 12500/2),
        ('Jane Fonda', 24500, 3, 24500/3),
        ('Judy Blume', 9500, 2, 9500/2),
        ('Joey Tribbiani', 9000, 1, 9000),
        ('Jenny Gump', 36550, 3, 36550/3)
        ]
    
    logger.info('Trying to Populate Initial Donor Data')
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                        donor_name = donor[DONOR_NAME],
                        donor_total = donor[DONOR_TOTAL],
                        donor_count = donor[DONOR_COUNT],
                        donor_average = donor[DONOR_AVERAGE]
                        )
                new_donor.save()
                logger.info('Donor population successful')
        
        # for saved in Donor:
            # print(f'{saved.donor_name} {saved.donor_total} {saved.donor_count} {saved.donor_average}')
    
    except Exception as e:
        logger.info(f'Error populating {donor[DONOR_NAME]}')
        logger.info(e)
        logger.info(f'Population of data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()    
        

        
def populate_initial_donations():
    """ Populate initial donation data """
    
    
    DONATION_DONOR = 0
    DONATION_AMOUNT = 1
    DONATION_DATE = 2
    
    donations = [
        ('John Travolta', 5000, '20180516'),
        ('John Travolta', 7500, '20180811'),
        ('Jane Fonda', 10000, '20180112'),
        ('Jane Fonda', 8000, '20180512'),
        ('Jane Fonda', 6500, '20180912'),
        ('Judy Blume', 3000, '20180601'),
        ('Judy Blume', 6500, '20181201'),
        ('Joey Tribbiani', 9000, '20180723'),
        ('Jenny Gump', 10300, '20181018'),
        ('Jenny Gump', 13750, '20181119'),
        ('Jenny Gump', 12500, '20181217')
        ]
    
    logger.info('Trying to Populate Initial Donation Data')
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                don_donor = donation[DONATION_DONOR].split()
                don_id = donation[DONATION_DATE] + "_" + don_donor[0][0:2] + don_donor[1][0:2]
                new_donation = Donation.create(
                        donation_donor = donation[DONATION_DONOR],
                        donation_amount = donation[DONATION_AMOUNT],
                        donation_date = donation[DONATION_DATE],
                        donation_id = don_id)
                new_donation.save()
                logger.info('Donation population successful')
        
        # for saved in Donation:
            # print(f'{saved.donation_id} {saved.donation_donor} {saved.donation_amount} {saved.donation_date}')
    
    except Exception as e:
        logger.info(f'Error populating donation of {donation[DONATION_AMOUNT]} from {donation[DONATION_DONOR]}')
        logger.info(e)
        logger.info(f'Population of data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()    
        
        
if __name__ == '__main__':
    populate_initial_donors()
    populate_initial_donations()        
