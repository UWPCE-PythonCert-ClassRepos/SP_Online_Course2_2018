"""
    Simple database example for mailroom project
    with Peewee ORM, sqlite and Python
    Use logging for messages so they can be turned off
"""
__author__ = "Wieslaw Pucilowski"

import logging
import string
from peewee import *
import pprint
pp = pprint.PrettyPrinter(width=120)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')
logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

database = SqliteDatabase('mailroom.db')
logger.info('Connecting to database...')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Donor(BaseModel):
    """
        This class defines Donor
    """
    logger.info('+++ Creating Class Donors')
    donor_name = CharField(primary_key=True, max_length=30)
    donor_location = CharField(null = True)
    

    def populate():
        """
        Populates Donor table
        """
        logger.info('+++ Working with Donor class')
        logger.info('+++ Populating Donor table with initial data')

        NAME = 0
        LOCATION = 1

        donors = [
                ('Speedy Gonzales', "New York"),
                ('Ivan Smirnoff', "Moscow"),
                ('Charles Goldberg', "Brooklyn"),
                ('Toshiro Asai', "Kioto"),
                ('Abdul Abdulah', "Dubai"),
                ('Pierre Leclerc', None),
            ]

        logger.info('Inserting Donor records:')

        try:
            # database.connect()
            # database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in donors:
                with database.transaction():
                    new_donor = Donor.create(
                                              donor_name = donor[NAME],
                                              donor_location = donor[LOCATION]
                                             )

                    logger.info('Donor {} was added to the database'.format(donor[NAME],
                                                                            donor[LOCATION])
                               )
                    new_donor.save()
    
        except Exception as e:
            logger.info('Error encounered creating {}'.format(donor))
            logger.info(e)
    
        finally:
            pass
            # logger.info('Database closes')
            # database.close()

class Donation(BaseModel):
    """
    This class defines donations.
    """

    logger.info('+++ Creating Donation Class')

    donor = ForeignKeyField(Donor, related_name='was_donated_by')
    amount = DecimalField(decimal_places = 2, null=True)

    def populate():
        """
        Populate Donation table
        """
        logger.info('+++ Working with Donation class')
        logger.info('+++ Populating Donation table with initial data')
        
        DONOR = 0
        AMOUNT = 1

        donations = [
                ('Speedy Gonzales', 10),
                ('Ivan Smirnoff', 20),
                ('Charles Goldberg', 30),
                ('Toshiro Asai', 40),
                ('Abdul Abdulah', 50),
                ('Speedy Gonzales', 100),
                ('Ivan Smirnoff', 200),
                ('Charles Goldberg', 300),
                ('Toshiro Asai', 400),
                ('Abdul Abdulah', 500),
                ('Speedy Gonzales', 1000),
                ('Ivan Smirnoff', 2000),
            ]

        try:
            # database.connect()
            # database.execute_sql('PRAGMA foreign_keys = ON;')
            for donation in donations:
                with database.transaction():
                    new_donation = Donation.create(
                                donor = donation[DONOR],
                                amount = donation[AMOUNT]
                            )
                    new_donation.save()
                logger.info('Adding Donor {} donated ${}'.format(donation[DONOR],
                                                          donation[AMOUNT]))
    
        except Exception as e:
            logger.info(f'Error creating = {donation[DONOR]}')
            logger.info(e)
    
        finally:
            pass

    def report():
        """
        Calculates NUMBER, TOTAL, AVERAGE of donations per Donor
        Updates Donor table: number, total, average
        """
        # CREATE VIEW Report AS
        # select donor_id, count(amount) as num, sum(amount) as total,  avg(amount) as avg from donation group by donor_id;
        
        logger.info('+++ Printing DB report')
        try:
            logger.info('Connecting to database...')
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Donation
                    .select(Donation.donor_id.alias('donor'),
                            fn.COUNT(Donation.donor_id).alias('num'),
                            fn.SUM(Donation.amount).alias('total'),
                            fn.AVG(Donation.amount).alias('avg'))
                    .group_by(Donation.donor_id)
            )
    
            pp.pprint('{:30} | {:20} | {:15} | {:15}'.format(
                                        'Donor',
                                        'Total',
                                        'Number',
                                        'Average')
                                )
            pp.pprint('='*89)
            for result in query:
                pp.pprint('{:30} | {:20} | {:15} | {:15}'.format(
                                                str(result.donor),
                                                str(result.num),
                                                str(result.total),
                                                str(result.avg)
                                            )
                       )

        except Exception as e:
            logger.info(e)
        finally:
            pass

# table createtion
logger.info('+++ Creating Tables in database')
database.create_tables([
        Donor,
        Donation
    ])

# tables initial population
logger.info('Populating tables...')
Donor.populate()
Donation.populate()
Donation.report()

logger.info('Closing database...')
database.close()
logger.info('SCHEMA created and tables populated...')