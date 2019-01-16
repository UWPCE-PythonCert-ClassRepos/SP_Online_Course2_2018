from create_mailroom_db import *

import logging
import pprint

a = 'Entry'
b = 'Donor'
c = 'ID'
d = 'Donation'
g = 'Total Donation'

def read_db():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mailroom.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
    query = (Donor
             .select(Donor, fn.SUM(Donation.amount).alias('total'), fn.COUNT(Donation.amount).alias('number'), Donation)
             .join(Donation, JOIN.INNER)
             .group_by(Donation)
             .order_by(Donor.donor_id)
            )
        
    logger.info(f'{a:<10} {b:<10} {c:<10} {d:<10} {g:<5}')
    logger.info(f'=' * 50)
    for donor in query:
        try:
            logger.info(f'{donor.donation.donation_id:<10} {donor.donor_name:<10} {donor.donor_id:<10} {donor.donation.amount:<10} {donor.total:<5}')
        except Exception as e:
            logger.info(f'{donor.donor_name} cannot be display properly...')
            logger.info(e)
    
    database.close()    

def donation_count():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mailroom.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
    query = (Donation
             .select(Donation)
            )
    
    database.close()
    return len(query)    
    
if __name__ == '__main__':
    read_db()