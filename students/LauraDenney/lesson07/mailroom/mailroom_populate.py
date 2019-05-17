'''This module creates SQL tables and populates db
with some data
'''

import logging
from mailroom_model import *
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database_Handler():
    '''this class adds, deletes, updates donor data in the
        database and runs queries'''
    database = SqliteDatabase('mailroom.db')

    def projection_query(self):
        '''select statement to get donations for projections'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            query = (Donation.select(Donation.donation,
                                     Donation.donor_donated
                                     ).order_by(Donation.donor_donated))
            projection_list = [x.donation for x in query]
        except Exception as e:
            logger.info(e)
        else:
            logger.info('query successful')
        finally:
            database.close()
            logger.info('closing database')
            return projection_list


    def report_query(self):
        '''select statement to get report values'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            query = (Donation.select(
                                Donation.donor_donated,
                                fn.sum(Donation.donation).alias('sum_donation'),
                                fn.count(Donation.donation).alias('count_donation')
                                ).group_by(Donation.donor_donated).order_by(
                                fn.sum(Donation.donation).desc()))
            report_list = [(x.donor_donated.full_name, x.sum_donation, x.count_donation) for x in query]
        except Exception as e:
            logger.info(e)
        else:
            logger.info('query successful')
        finally:
            logger.info('closing database')
            database.close()
            return report_list


    def letter_query(self):
        '''select statement to get thank you letters values'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            query = (Donation.select(
                                Donation.donor_donated,
                                fn.sum(Donation.donation).alias('sum_donation')
                                ).group_by(Donation.donor_donated))
            report_list = [(x.donor_donated.full_name, x.sum_donation) for x in query]
        except Exception as e:
            logger.info(e)
        else:
            logger.info('query successful')
        finally:
            logger.info('closing database')
            database.close()
            return report_list


    def is_current_donor(self, donor):
        '''query to check if donor exists in database'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            query = Donor.select(Donor.full_name).where(Donor.full_name == donor)
        except Exception as e:
            logger.info(e)
        finally:
            logger.info('closing database')
            #if donor in query length will be 1
            if len(query):
                database.close()
                logger.info('donor exists')
                return True
            else:
                database.close()
                logger.info('donor does not exist')
                return False

    def is_current_donation(self, donor, donation):
        '''query to check if donor and donation exist in Donation'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            query = Donation.get(
                            (Donation.donor_donated == donor) &
                            (Donation.donation == donation))
        except Exception as e:
            logger.info(e)
            logger.info('{} donation does not exist for {}'.format(donation, donor))
            database.close()
            logger.info('closing database')
            return False
        #if donation in query no Error is raised
        else:
            logger.info('donation exists')
            database.close()
            logger.info('closing database')
            return True

    def update_donation(self, donor, donation):
        '''changes a donation amount in Donation'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            adonation = Donation.get(
                            (Donation.donor_donated == donor) &
                            (Donation.donation == donation))
            adonation.donation = donation
            adonation.save()
        except Exception as e:
            logger.info(e)
        else:
            logger.info('update successful')
        finally:
            logger.info('closing database')
            database.close()

    def get_list(self):
        '''select statement to get all full names of donors'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            query = Donor.select()
            names = [donor.full_name.title() for donor in query]
        except Exception as e:
            logger.info(e)
        else:
            logger.info('query successful')
        finally:
            logger.info('closing database')
            database.close()
            return names

    def remove_donor(self, donor_name):
        '''removes donor information from all tables'''
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            donation_delete_query = Donation.delete().where(Donation.donor_donated==donor_name)
            donor_query = Donor.get(Donor.full_name==donor_name)

            logger.info("Deleting donation instances")
            donation_delete_query.execute()

            logger.info('Deleting Donor instance.')
            donor_query.delete_instance()
        except Exception as e:
            logger.info(e)
        else:
            logger.info('delete successful')
        finally:
            logger.info('Closing database')
            database.close()

    def add_donor(self, donor_name):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            #formatting for one word names
            first_last = donor_name.split(" ")
            if len(first_last) == 1:
                first = first_last[0]
                last = None
            else:
                first = first_last[0]
                last = first_last[1]

            new_donor = Donor.create(
                first_name = first,
                last_name = last,
                full_name = donor_name)
            new_donor.save()
        except Exception as e:
            logger.info(e)
        else:
            logger.info('Donor added to Database')
        finally:
            database.close()
            logger.info('closing database')

    def add_donation(self, amount, name):
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            logger.info('connecting to database')

            new_donation = Donation.create(
                donation = amount,
                donor_donated = name,
                date_donation = date.today().isoformat())
            new_donation.save()
        except Exception as e:
            logger.info(e)
        else:
            logger.info('Donation added to Database')
        finally:
            database.close()
            logger.info('closing database')

def first_run():
    '''creates and populates database'''
    create_tables()
    populate_donor()
    populate_donation()

def create_tables():
    '''creates database tables'''
    database = SqliteDatabase('mailroom.db')
    try:
        logger.info('connecting to database')
        database.connect()
        logger.info('Creating tables in database')
        database.create_tables([
            Donor,
            Donation])
    except Exception as e:
        logger.info('Error: ', e)
    else:
        logger.info('successfully added tables')
    finally:
        database.close()


def populate_donor():
    '''add donor data to database'''
    database = SqliteDatabase('mailroom.db')

    FIRST_NAME = 0
    LAST_NAME = 1

    donors = [
        ('john', 'doe'),
        ('laura', 'denney'),
        ('bill', 'gates'),
        ('samuel', 'jackson'),
        ('mr.','bean')]

    try:
        database.connect()
        logger.info('Connecting to Database')
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('attempting adding data to Donor')
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                    first_name = donor[FIRST_NAME],
                    last_name = donor[LAST_NAME],
                    full_name = '{} {}'.format(donor[FIRST_NAME],
                                               donor[LAST_NAME]))
                new_donor.save()

    except Exception as e:
        logger.info('Error: ', e)
    else:
        logger.info('Database add successful')
    finally:
        database.close()
        logger.info('closing database')


def populate_donation():
    '''add donation data to database'''
    database = SqliteDatabase('mailroom.db')

    DONATION = 0
    DONOR_DONATED = 1
    DATE_DONATION = 2

    donations = [
        (100.50, 'john doe', '2017-12-12'),
        (200.00, 'john doe', '2018-01-13'),
        (5.00, 'laura denney', '2005-08-31'),
        (4000, 'bill gates', '2010-07-17'),
        (1, 'samuel jackson', '2008-05-04'),
        (2, 'samuel jackson', '2005-05-04'),
        (3, 'samuel jackson', '2006-05-04'),
        (500, 'mr. bean', '2009-10-21'),
        (100, 'mr. bean', '2007-12-12')]

    try:
        database.connect()
        logger.info('Connecting to Database')
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('attempting adding data to Donation')
        for donation in donations:
            with database.transaction():
                new_donation = Donation.create(
                    donation = donation[DONATION],
                    donor_donated = donation[DONOR_DONATED],
                    date_donation = donation[DATE_DONATION])
                new_donation.save()

    except Exception as e:
        logger.info('Error: ', e)
    else:
        logger.info('Database add successful')
    finally:
        database.close()
        logger.info('closing database')