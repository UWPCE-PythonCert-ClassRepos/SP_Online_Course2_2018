from peewee import *
from create_database import *
import logging
import decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def donor_input():
        return input("Enter a donor name, input 'List'"+
                     " for a list of donors, select 'Delete' to remove "+
                     "a donor from the database, or 'Reenter' to change a donation\n>")

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
        elif don_input.lower() == "delete":
            list_donors()
            remove = input("Enter a donor name to remove "+
                     "a donor from the database\n>")
            delete_donor(remove)
            don_input = None
        elif don_input.lower()== "reenter":
            list_donors()
            rename = input("Enter a donor name to change "+
                     "a donation in the database\n>")
            reenter_donation(rename)
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

def delete_donor(donor):
    database = SqliteDatabase('donor_database.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            search = Donors.get(Donors.donor_name == donor)
            search.delete_instance()
            search_donation = Donations.get(Donations.d_name == donor)
            search_donation.delete_instance()
            logger.info('Donor {} was deleted from the database'.format(donor))
    except Exception as e:
        logger.info('Error deleting {} from database'.format(donor))
        logger.info(e)
    finally:
        logger.info('Updating Database')
        update_donations()
        logger.info('Database closes')
        database.close()

def reenter_donation(donor):
    old = float(input("Enter the old donation amount\n>"))
    new = donation_prompt()
    database = SqliteDatabase('donor_database.db')
    try:
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            search = Donations.get((Donations.d_name_id == donor) &
                                           (Donations.d_amount == old))
            search.d_amount = new
            search.save()
            for donor in Donors:
                x = Donations.select().where(Donations.d_name_id == donor)
                number_of_donations = x.count()
                total = decimal.Decimal('0.0')
                for item in x.iterator():
                    total += item.d_amount
                donor.total_donation = total
                donor.number_donation = number_of_donations
                donor.ave_donation = total/number_of_donations
                donor.save()
    except Exception as e:
        logger.info('Error changing donation for {} in database'.format(donor))
        logger.info(e)
    finally:
        logger.info('Updating Database')
        update_donations()
        logger.info('Database closes')
        database.close()

def close_program():
    print('\nClosing Program\n')
