
from mailroom_db_frame import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_donors():
    """
    Populate the donor frame
    """

    database = SqliteDatabase('mailroom.db')
    logger.info('Initializing Donor Class'.format(database))    

    donors = ['Justin Thyme',
              'Beau Andarrow',
              'Crystal Clearwater',
              'Harry Shins', 
              'Bob Zuruncle',
              'Al Kaseltzer',
              'Joe Somebody']

    logger.info('Creating Donor List DB')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                    donor_name = donor
                )
                logger.info('{} was added to db'.format(donor))
    except Exception as e:
        logger.error('Unable to create a record for {}. \n Error:{}'.format(donor, e))
    finally:
        database.close()


def populate_donations():
    """
    Popluate the donations frame
    """
    database = SqliteDatabase('mailroom.db')
    logger.info('Databse {} is initialized'.format(database))

    DONOR_NAME = 0
    DONATION_AMOUNT = 1

    donations = [('Justin Thyme', 1), ('Justin Thyme', 1), ('Justin Thyme', 1),
                 ('Beau Andarrow', 207.12), ('Beau Andarrow', 400.32), ('Beau Andarrow', 12345),
                 ('Crystal Clearwater', 80082),
                 ('Harry Shins', 1), ('Harry Shins', 2), ('Harry Shins', 3), 
                 ('Bob Zuruncle', 0.53), ('Bob Zuruncle', 7.00),
                 ('Al Kaseltzer', 1010101), ('Al Kaseltzer', 666.00),
                 ('Joe Somebody', 25)]

    logger.info('Creating donors records')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donation in donations:
            with database.transaction():
                new_donation = Donations.create(
                    donation_name=donation[DONOR_NAME],
                    donation_amount=donation[DONATION_AMOUNT]
                )
                logger.info('Donation {} for donor: {} was added to db'.format(
                    donation[DONATION_AMOUNT], donation[DONOR_NAME]))
    except Exception as ex:
        logger.error('Unable to create a record for {}. Err: {}'.format(donation, ex))
    finally:
        database.close()


def update_donors():
    """update the donor frame to reflect current donation totals"""
    database = SqliteDatabase('mailroom.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in Donor:
            don_matches = Donations.select().where(Donations.donation_name_id == donor)
            number_of_donations = don_matches.count()
            logger.info('{} has made {} donations'.format(donor, number_of_donations))
            total = 0.0
            for item in don_matches.iterator():
                logger.info(item.donation_amount)
                total += item.donation_amount
            logger.info('{} has donated a total of ${}'.format(donor, total))
            donor.number_of_donations = number_of_donations
            donor.donation_total = total
            donor.save()
    except Exception as ex:
        logger.error('Unable to get donors. Err: {}'.format(ex))
    finally:
        database.close()


if __name__ == '__main__':
    populate_donors()
    populate_donations()
    update_donors()