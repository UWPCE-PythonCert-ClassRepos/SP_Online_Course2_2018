"""
    Default database for testing mailroom
"""
import logging
from create_mailroom import *

def populate_db():
    """
    add data to database for testing the mailroom
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mail_default.db')
    
    logger.info('Working with Donor class')
    DONATOR = 0
    DONATION = 1
        
    donations = [
        ('Andrew', 300),
        ('Janet', 250),
        ('Joshua', 120.20),
        ('Melanie', 320.21),
        ('Tatsiana', 29.29)
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for name in donations:
            with database.transaction():
                new_donor = Donor.create(
                    donor_name=name[DONATOR],
                    donations=name[DONATION]
                    )
                new_donor.save()
                
        for saved_donor in Donor:
            logger.info(f'{saved_donor} has donated {saved_donor.donations}.')
                            
    except Exception as e:
        logger.info(e)
        logger.info(f'Error creating = {name[DONATOR]}')
    finally:
        database.close()
        
def populate_details():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mail_default.db')
    
    logger.info('Working with Details')

    NAME = 0
    TRANSACTIONS = 1
    TOTAL = 2
    AVERAGE = 3
    FIRST_GIFT = 4
    LAST_GIFT = 5

    details = [
        ('Andrew', 1, 300, 300, 300, 300),
        ('Janet', 1, 250, 250, 250, 250),
        ('Joshua', 1, 120.20, 120.20, 120.20, 120.20),
        ('Melanie', 1, 320.21, 320.21, 320.21, 320.21),
        ('Tatsiana', 1, 29.29, 29.29, 29.29, 29.29)
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for detail in details:
            with database.transaction():
                new_details = Details.create(
                    name=detail[NAME],
                    transactions=detail[TRANSACTIONS],
                    total=detail[TOTAL],
                    average=detail[AVERAGE],
                    first_gift=detail[FIRST_GIFT],
                    last_gift=detail[LAST_GIFT]
                    )
                new_details.save()
                
        for det in Details:
            logger.info(f'{det}-transactions:{det.transactions} total:{det.total} ' +\
                f'average:{det.average} first_gift:{det.first_gift} last_gift:{det.last_gift}')

    except Exception as e:
        logger.info(e)
        logger.info(f'Error creating = {detail[NAME]}')
    finally:
        database.close()


if __name__ == '__main__':
    populate_db()
    populate_details()