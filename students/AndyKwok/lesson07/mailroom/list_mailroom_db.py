from create_mailroom_db import *

import logging
import pprint

a = 'Donation ID'
b = 'Donor Name'
c = 'Donor ID'
d = 'Donation Amount'
g = 'Total Donation'

def read_db_select(donorname):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mailroom.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
    query = (Donor
             .select(Donor, Donation)
             .join(Donation, JOIN.LEFT_OUTER)
             .group_by(Donation)
             .order_by(Donor.donor_id)
            )
        
    logger.info(f'{c:<15} {b:<15} {a:<15} {d:<15}')
    logger.info(f'=' * 55)
    for donor in query.where(Donor.donor_name == donorname):
        try:
            logger.info(f'{donor.donor_id:<15} {donor.donor_name:<15} {donor.donation.donation_id:<15} {donor.donation.amount:<15}')
        except Exception as e:
            logger.info(f'{donor.donor_name} cannot be display properly...')
            logger.info(e)
    
    database.close()
    
def read_db_total():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mailroom.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
    query = (Donor
             .select(Donor, fn.SUM(Donation.amount).alias('total'))
             .join(Donation, JOIN.LEFT_OUTER)
             .group_by(Donor)
             .order_by(Donor.donor_id)
            )
        
    print(f'{c:<15} {b:<15} {g:<15}')
    print(f'=' * 50)
    for donor in query:
        try:
            print(f'{donor.donor_id:<15} {donor.donor_name:<15} {donor.total:<15}')
        except Exception as e:
            logger.info(f'{donor.donor_name} cannot be display properly...')
            logger.info(e)
    
    database.close()
    
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
        
    logger.info(f'{c:<15} {b:<15} {a:<15} {d:<15} {g:<15}')
    logger.info(f'=' * 50)
    for donor in query:
        try:
            logger.info(f'{donor.donor_id:<10} {donor.donor_name:<10} {donor.donation.donation_id:<10} {donor.donation.amount:<10} {donor.total:<5}')
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