import donors_sql as d
from create_mr_tables import *


connect = d.Individual('mailroom.db')

database.connect()
logger.info('Connected to database')
database.execute_sql('PRAGMA foreign_keys = ON;')

donors=['Shane', 'Pete', 'Zach', 'Joe', 'Fitz']
donations = [('Shane', 6), ('Shane', 5), ('Shane', 10), ('Joe', 5), ('Zach',10)]

try:
    for donor in donors:
        with database.transaction():
            logger.info(f'Trying to add new donor {donor}.')
            new_donor = Donor.get_or_create(donor_name=donor)
            #new_donor.save()
            logger.info(f'Success adding donor {donor}.')
except Exception as e:
    logger.info(f'Error loading database')
    logger.info(e)
    logger.info('Failed to add new donor.')
finally:

    logger.info('Completed loading donors')


try:
    for donation in donations:
        with database.transaction():
            logger.info('Trying to add new donation.')
            new_donation = Donations.create(
                donor_name=donation[0],
                donation=donation[1])
            new_donation.save()
            logger.info(f'Database added a donation of '
                        f'{donation[0]} by {donation[1]}.')
except Exception as e:
    logger.info(f'Error loading donations')
    logger.info(e)
    logger.info('Failed to add donations.')
finally:

    logger.info('database closes')
    database.close()
