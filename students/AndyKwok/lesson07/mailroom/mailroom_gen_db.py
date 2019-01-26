from create_mailroom_db import *

import logging

def add_donor(adddonor):
    """
        demonstrate how database protects data inegrity : add
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')    

    DONOR_NAME = 0
    DONOR_ID = 1
    
    try:
        for person in adddonor:
            with database.transaction():
                new_donor = Donor.create(
                    donor_name = person[DONOR_NAME],
                    donor_id = person[DONOR_ID])      
                new_donor.save()
                logger.info('Donor was added to database successfully...')
    except Exception as e:
        logger.info('Person {new_donor.donor_name} was not added...')
        logger.info(e)
    finally:
        database.close()
        
def add_donation(donations):
    """
        demonstrate how database protects data inegrity : add
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')
    
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
    AMOUNT = 0
    DONATION_ID = 1
    DONATED_BY = 2
        
    try:
        for person in donations:
            with database.transaction():
                new_donation = Donation.create(
                        amount = person[AMOUNT],
                        donation_id = person[DONATION_ID],
                        donated_by = person[DONATED_BY])      
                new_donation.save()
                logger.info('Donation was added to database successfully...')
    except Exception as e:
        logger.info('Donation was not added...')
        logger.info(e)
    finally:
        database.close()        

def edit_donation(id , new_amount):
    """
        demonstrate how database protects data inegrity : add
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')  
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
        
    try:
        with database.transaction():
            adonation = Donation.get(Donation.donation_id == id)
            adonation.amount = new_amount      
            adonation.save()
            logger.info('Donation was updated in the database...')
    except Exception as e:
        logger.info('Donation entry was not edited...')
        logger.info(e)  
    finally:
        database.close()     
  
def delete_donor(id):
    """
        demonstrate how database protects data inegrity : delete
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('mailroom.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    try:
        with database.transaction():
            adonor = Donor.get(Donor.donor_id == id)
            logger.info(f'Trying to delete {adonor.donor_name}')
            query = Donation.delete().where(Donation.donated_by == id)
            query.execute()
            adonor.delete_instance()
            logger.info('Donor was deleted from the database...')
    except Exception as e:
        #logger.info(f'Delete failed: {adonor.donor_name}')
        logger.info(e)
    finally:
        database.close()        
        
def delete_donation(id):
    """
        demonstrate how database protects data inegrity : delete
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('mailroom.db')
    
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
 
    try:
        with database.transaction():
            adonation = Donation.get(Donation.donation_id == id)
            logger.info(f'Trying to delete {adonation.donation_id}')
            adonation.delete_instance()
            logger.info('Donation entry was removed from the database...')
    except Exception as e:
        logger.info(f'Delete failed: {adonor.donation_id}')
        logger.info(e)

    finally:
        database.close()                

if __name__ == '__main__':
    add_donor()
    add_donation()