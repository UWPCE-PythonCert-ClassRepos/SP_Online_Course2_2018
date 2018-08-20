from peewee import *
from create_database import *
import logging
import decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def donor_input():
        return input("Enter a donor name or input 'List'"+
                     " for a list of donors\n>")

def donation_prompt():
    return input("Enter a donation amount \n>")

def update_donations():

    database = SqliteDatabase('donor_database.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for donor in Donors:
            x = Donations.select().where(Donations.d_name_id == donor)
            number_of_donations = x.count()
            logger.info('{} has {} donations'.format(donor, number_of_donations))
            total = decimal.Decimal('0.0')
            for item in x.iterator():
                total += item.d_amount
            logger.info('{} has donated a total of {}'.format(donor, total))
            donor.total_donation = total
            donor.number_donation = number_of_donations
            donor.ave_donation = total/number_of_donations
            donor.save()

    except Exception as e:
        logger.error('Unable to get donors')
        logger.info(e)

    finally:
        database.close()

def list_donors():
    database = SqliteDatabase('donor_database.db')
    donor_list = []
    logger.info('Printing List')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for x in Donors.select():
            donor_list.append(x.donor_name)
            logger.info('{}'.format(x.donor_name))
        return donor_list
    except Exception as e:
        logger.error('Unable to gather donor list')
        logger.error(e)
    finally:
        database.close()

def add_donor(donor):
    database = SqliteDatabase('donor_database.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            new_donor = Donors.create(donor_name = donor)
            logger.info('Donor {} was added to the database'.format(donor))
    except Exception as e:
        logger.info('Error creating = {}'.format(donor))
        logger.info(e)
    finally:
        logger.info('Updating Database')
        update_donations()
        logger.info('Database closes')
        database.close()

def add_donation(donation):
    database = SqliteDatabase('donor_database.db')

    DONOR_NAME = 0
    DONOR_DONATION = 1

    logger.info('Creating Donation records:')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            new_donation = Donations.create(
                d_name = donation[DONOR_NAME],
                d_amount = donation[DONOR_DONATION])
            new_donation.save()
        logger.info('Donor {} donated ${}'.format(donation[DONOR_NAME],
                                                      donation[DONOR_DONATION]))

    except Exception as e:
        logger.info(f'Error creating = {donation[DONOR_NAME]}')
        logger.info(e)

    finally:
        logger.info('Database closes')
        database.close()

def get_donor_total(donor):
    database = SqliteDatabase('donor_database.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        x = Donors.select().where(Donors.donor_name == donor)
        for item in x:
            return item.total_donation
    except Exception as e:
        logger.info('Error creating = {}'.format(donor))
        logger.info(e)
    finally:
        database.close()

def send_thankyou():
    don_input = None
    while not don_input:
        don_input = donor_input()
        if don_input.lower() == "list":
            list_donors()
            don_input = None
        
    donation = None
    while not donation:
        try:
            donation = donation_prompt()
        except ValueError:
            print("Enter donations numerically")
    
    add_donor(don_input)
    add_donation((don_input, donation))
        
    print("Thank you {} for your donation of ${}"
              .format(don_input, donation))

def send_thankyou_total(donor):
    return ("Dear Ms./Mrs./Mr./Dr. {}, \n We are thankful for your donation of ${}. ".format(donor.donor_name, get_donor_total(donor)) +
            "Your donation will be used for (insert harmful activity here). " +
            "We hope you donate again soon!")

def create_report():
    update_donations()
    print('{:20} | {:15} | {:10} | {:15}'.format(
        'Donor Name', 'Total Given', 'Num Gifts', 'Average Gift'))
    print('-'*70)
    for donor in Donors.select():
        try:
            print('{:20} | {:15} | {:10} | {:15}'.format(
                donor.donor_name, donor.total_donation,
                donor.number_donation,
                donor.ave_donation))
        except TypeError:
            pass

def send_letters():
    for donor in Donors.select():
            with open(donor.donor_name + '.txt', 'w') as donorfh:
                donorfh.write(send_thankyou_total(donor))

def close_program():
    print('\nClosing Program\n')
