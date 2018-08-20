from mailroom_db import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def update_donations():
    database = SqliteDatabase('mailroom.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in Donor:
            x = Donations.select().where(Donations.d_name_id == donor)
            number_of_donations = x.count()
            logger.info('{} has {} donations'.format(donor, number_of_donations))
            total = 0.0
            for item in x.iterator():
                logger.info(item.donation_amount)
                total += item.donation_amount
            logger.info('{} has donated a total of {}'.format(donor, total))
            donor.number_of_donations = number_of_donations
            donor.total_donations = total
            donor.save()
    except Exception as ex:
        logger.error('Unable to get donors. Err: {}'.format(ex))
    finally:
        database.close()


def list_donors():
    database = SqliteDatabase('mailroom.db')
    all_donors = []
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for x in Donor.select():
            all_donors.append(x.donor_name)
        return all_donors
    except Exception as ex:
        logger.error('Unable to get donors. Err: {}'.format(ex))
    finally:
        database.close()


def get_total_for_donor(donor):
    database = SqliteDatabase('mailroom.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        x = Donor.select().where(Donor.donor_name == donor)
        for item in x:
            return item.total_donations
    except Exception as ex:
        logger.error('Unable to get donors. Err: {}'.format(ex))
    finally:
        database.close()


def send_thankyou(donor):
    print('Thank you {} for your generous donation of {}'.format(
        donor, get_total_for_donor(donor)
    ))


def add_donor(donor):
    database = SqliteDatabase('mailroom.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            new_donor = Donor.create(
                donor_name=donor
            )
            logger.info('Donor {} was added to db'.format(donor))
    except Exception as ex:
        logger.error('Unable to create a record for {}. Err: {}'.format(donor, ex))
    finally:
        update_donations()
        database.close()


def create_report():
    print('{:20} | {:15} | {:10} | {:15}'.format(
        'Donor Name', 'Total Given', 'Num Gifts', 'Average Gift'))
    print('-'*70)
    for donor in Donor.select():
        try:
            avg = donor.total_donations / donor.number_of_donations
        except ZeroDivisionError:
            avg = 0
        except TypeError:
            pass
        try:
            print('{:20} | {:15} | {:10} | {:15}'.format(
                donor.donor_name, donor.total_donations,
                donor.number_of_donations,
                avg))
        except TypeError:
            pass


def save_report():
    for donor in list_donors():
        with open(donor + '.txt', 'w') as donorfh:
            try:
                donorfh.write(send_thankyou(donor))
            # In case a donor has no donations
            except TypeError:
                pass