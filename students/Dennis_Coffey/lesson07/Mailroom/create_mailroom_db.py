"""
    Dennis Coffey
    4/1/2019
    Donor class used to populate donors for mailroom
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')

logger.info('This means we can easily switch to a different database')
logger.info('Enable the Peewee magic! This base class does it all')
logger.info('By inheritance only we keep our model (almost) technology neutral')

# Define database
database = SqliteDatabase('donors.db')

class BaseModel(Model):
    class Meta:
        database = database

class Donor(BaseModel):
    """
        This class defines Donor.
    """

    logger.info('Defining attribute of Donor class')
    donor_id = IntegerField(primary_key = True)
#    donor_id = IntegerField()
    donor_name = CharField(max_length = 30)

class Donation(BaseModel):
    """
        This class defines each Donation by a donor.
    """
    logger.info('Donation ID')
    donation_id = IntegerField(primary_key = True)
    logger.info('Donor name')
    donor_name = CharField(max_length = 30)
#    donor_name = ForeignKeyField(Donor, related_name='was_filled_by', null=False)
    logger.info('Donation amount')
    donation_amount = DecimalField(max_digits = 15, decimal_places = 2, null=False)
    
    # Create email to donor thanking them for their generous donation
    def create_email(self, amount):
        return '\nDear {},\n\nThank you so much for generous donation of ${}.\n\n\t\t\tSincerely,\n\t\t\tPython Donation Team'.format(self.donor_name, amount)

    
def populate_donors(donors):
    """
    Add donor data to the database
    """

    logger = logging.getLogger(__name__)
    logger.info('Working with Donor class')

    DONOR_ID = 0
    DONOR_NAME = 1
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        # Loop through departments list and insert into database
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                        donor_id = donor[DONOR_ID],
                        donor_name = donor[DONOR_NAME])
                new_donor.save()

    except Exception as e:
        logger.info(f'Error creating {donor[DONOR_ID]} in database')
        logger.info(e)
        
    finally:
        logger.info('Database closes')
        database.close()

def populate_donations(donations):
    """
    Add donation data to the database
    """

    logger = logging.getLogger(__name__)
    logger.info('Working with Donation class')

    DONATION_ID = 0
    DONOR_NAME = 1
    DONATION_AMOUNT = 2
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        # Loop through departments list and insert into database
        for donation in donations:
            with database.transaction():
                new_donation = Donation.create(
                        donation_id = donation[DONATION_ID],
                        donor_name = donation[DONOR_NAME],
                        donation_amount = donation[DONATION_AMOUNT])
                new_donation.save()

    except Exception as e:
        logger.info(f'Error creating {donation[DONATION_ID]} in database')
        logger.info(e)
        
    finally:
        logger.info('Database closes')
        database.close()



if __name__ == '__main__':

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only
    
    # Create table and structure
    database.create_tables([
            Donor,
            Donation
        ])
    
    # Close database
    database.close()

    # List of donors to load into database
    donors = [(1,'Dennis Coffey'),
                  (2, 'Bill Gate'),
                  (3, 'Ethan Coffey'),
                  (4, 'Paul Allen'),
                  (5, 'Jeff Bezos')]
    
    # Load donors into database
    populate_donors(donors)

    # List of donations to load into database
    donations = [(1, 'Dennis Coffey', 2500.00),
                 (2, 'Dennis Coffey', 400.00),
                 (3, 'Dennis Coffey', 1400.00),
                 (4, 'Dennis Coffey', 4000.00),
                 (5, 'Dennis Coffey', 75.00),
                 (6, 'Bill Gates', 120.00),
                 (7, 'Bill Gates', 650.00),
                 (8, 'Bill Gates', 40.00),
                 (9, 'Bill Gates', 75.00),
                 (10, 'Ethan Coffey', 800.00),
                 (11, 'Ethan Coffey', 150.00),
                 (12, 'Ethan Coffey', 1100.00),
                 (13, 'Ethan Coffey', 2000.00),
                 (14, 'Ethan Coffey', 60.00),
                 (15, 'Paul Allen', 400.00),
                 (16, 'Paul Allen', 45000.00),
                 (17, 'Paul Allen', 9000.00),
                 (18, 'Jeff Bezos', 3.00),
                 (19, 'Jeff Bezos', 8.00)]

    # Load donations into database
    populate_donations(donations)

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        sorted_donors = (Donation
                 .select(Donation.donor_name,
                         fn.MAX(Donation.donation_amount).alias('last_donation'))
                 .group_by(Donation.donor_name)
                 .order_by(Donation.donor_name))
        
    except Exception as e:
        logger.info(f'Error retrieving donors last donation from database')
        logger.info(e)
        
    finally:
        print('Database closed - send')
        database.close()
        
    print('Print list of donors')
    for donor in sorted_donors:
        print(donor.donor_name)
