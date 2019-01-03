"""
    Default database for testing mailroom
"""
import logging
from .create_mailroom import *

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
        ('Andrew', 500),
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
        
def populate_donos():
    """
    add donos for testing the mailroom
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mail_default.db')
    
    logger.info('Working with Donation class')
    HELD_BY = 0
    DONO = 1
    DONO_SIZE = 2
    DONO_NUMBER = 3
    
    donations = [
        ('Andrew', 300, 'Large', 1),
        ('Andrew', 200, 'Large', 2),
        ('Janet', 250, 'Large', 3),
        ('Joshua', 120.20, 'Small', 4),
        ('Melanie', 320.32, 'Large', 5),
        ('Tatsiana', 29.29, 'Small', 6)
        ]
        
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                new_dono = Donation.create(
                    held_by=donation[HELD_BY],
                    dono=donation[DONO],
                    dono_size=donation[DONO_SIZE],
                    dono_number=donation[DONO_NUMBER]
                    )
                new_dono.save()
                
        for saved_donation in Donation:
            logger.info(f'{saved_donation.held_by} made a donation of {saved_donation.dono}')
            
    except Exception as e:
        logger.info(e)
        logger.info(f'Error creating ={donation[HELD_BY]}')
    finally:
        database.close()
        
def populate_details():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mail_default.db')
    
    logger.info('Working with Details')

    NAME = 0
    TRANSACTIONS = 1
    AVERAGE = 2
    FIRST_GIFT = 3
    LAST_GIFT = 4

    details = [
        ('Andrew', 2, 250, 300, 200),
        ('Janet', 1, 250, 250, 250),
        ('Joshua', 1, 120.20, 120.20, 120.20),
        ('Melanie', 1, 320.21, 320.21, 320.21),
        ('Tatsiana', 1, 29.29, 29.29, 29.29)
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for detail in details:
            with database.transaction():
                new_details = Details.create(
                    name=detail[NAME],
                    transactions=detail[TRANSACTIONS],
                    average=detail[AVERAGE],
                    first_gift=detail[FIRST_GIFT],
                    last_gift=detail[LAST_GIFT]
                    )
                new_details.save()
                
        for det in Details:
            logger.info(f'{det}-transactions:{det.transactions} ' +\
                f'average:{det.average} first_gift:{det.first_gift} last_gift:{det.last_gift}')

    except Exception as e:
        logger.info(e)
        logger.info(f'Error creating = {detail[NAME]}')
    finally:
        database.close()


if __name__ == '__main__':
    populate_db()
    populate_donos()
    populate_details()