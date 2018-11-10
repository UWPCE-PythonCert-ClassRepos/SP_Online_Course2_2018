#!/usr/bin/env python3
"""This module contains all of the database specific operations for the
    Peewee Database Mail Room
"""
import decimal
import logging
from datetime import datetime
from peewee import *
from mailroom_model import *
from pprint import pprint as pp

database = SqliteDatabase('donor_database.db')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#SQL calls for lists in mailroom
def get_all_donor_totals():
    """ Calls DB to calculate count of donations for single donor"""
    try:
        logger.info('opening get_all_donor_totals database call')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query_totals = (Donations
                        .select(Donations.donated_by_id.alias('fullname'),
                                fn.COUNT(Donations.donated_by_id).alias(
                                    'num_donations'),
                                fn.sum(Donations.donation_amount).alias('donation_total'))
                        .group_by(Donations.donated_by_id)
                        )
        return query_totals
    except Exception as e:
        logger.info(f'Error getting list of donors')
        logger.info(e)

    finally:
        logger.info('closing get_all_donor_totals database call')
        database.close()

def get_list_of_donors():
    """
    Gets the donors from the database
    """
    try:
        logger.info('opening get_list_of_donors database call')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        return Donors.select()

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

def get_max_donation_date_list():
    """
    Gets the record for each donor for the max(date)
    """
    try:
        logger.info('opening get_max_donation_date_list database call')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query_max_date = (Donations
                          .select(Donations.donated_by_id.alias('fullname'),
                                  fn.MAX(Donations.donation_date).alias(
                                      'last_donation_date'),
                                  Donations.donation_amount.alias('last_donation'))
                          .group_by(Donations.donated_by_id)
                          )
        return query_max_date

    except Exception as e:
        logger.info(e)

    finally:
        database.close()
        logger.info('closing get_max_donation_date_list database call')

def get_list_of_donations():
    """Gets a full list of donations from the database"""
    try:
        logger.info('opening get_list_of_donations database call')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query_results = (Donations.select(Donations.id, Donations.donation_date,
                                          Donations.donation_amount, Donations.donated_by_id.alias('fullname')))
        return query_results
    except Exception as e:
        logger.info(f'Error getting list of donors')
        logger.info(e)

    finally:
        logger.info('closing get_list_of_donations database call')
        database.close()

#Actions on the db to add/delete/change
def add_donor(donor_firstname, donor_lastname, donor_fullname):
    """
    Adds donor to database if donor isn't already in the db
    """
    try:
        logger.info('opening add_donor database call')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        new_donor = Donors.create(
            firstname=donor_firstname,
            lastname=donor_lastname,
            fullname=donor_fullname
        )
        new_donor.save()
    except IntegrityError:
        logger.info(f'This donor is already in our database: {donor_firstname}'
                    f'{donor_lastname}')
    finally:
        logger.info('closing add_donor database call')
        database.close()


def add_donation(donor_name, donation):
    """
    Add a donation record to the donation table.
    """
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        new_donation = Donations.create(
            donation_date=datetime.today(),
            donation_amount=decimal.Decimal(donation),
            donated_by=donor_name
        )
        new_donation.save()
        logger.info(f'Saving {donor_name} - {donation}')
    except Exception as ex:
        logger.info(f'Error creating {new_donation[donation]} for {new_donation.donated_by.firstname}'
                    + f' {new_donation.donated_by.lastname}')
        logger.info(ex)

    finally:
        database.close()

# def get_list_of_donations_challenge(min_don, max_don):
#     """Gets a full list of donations from the database"""
#     try:
#         logger.info('opening get_list_of_donations database call')
#         database.connect()
#         database.execute_sql('PRAGMA foreign_keys = ON;')
#         query_results = (Donations
#                          .select()
#                          .where((Donations.donation_amount > min_don) &
#                                 (Donations.donation_amount < max_don)
#                                 ))
# #        for x in query_results:
# #            logger.info(f'{x.donated_by_id} - amount: {x.donation_amount} - total: {x.donation_date}')
#         return query_results
#     except Exception as e:
#         logger.info(f'Error getting list of donors')
#         logger.info(e)

#     finally:
#         logger.info('closing get_list_of_donations database call')
#         database.close()


def change_donation(donor_name, old_donation, donation_update):
    """
    Changes a donation record in the donations table (can be used to update date, time , or donor of this record)
    """
    try:
        logger.info('Opening change_donation database connection')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            donation_search = Donations.get((Donations.donation_amount == old_donation) &
                (Donations.donated_by_id==donor_name))
            donation_search.donation_amount = donation_update
            donation_search.save()
            logger.info(f'Updated {donor_name}\'s donation from {old_donation} to {donation_update}')

    except Exception as e:
        logger.info('Error updating {} donation in database'.format(donor_name))
        logger.info(e)
    finally:
        logger.info('Closing change_donation database connection')
        database.close()


def delete_donation_from_db(donor_name, donation_amount):
    try:
        logger.info('Opening delete_donation_from_db database connection')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            donation_db = Donations.get((Donations.donated_by_id == donor_name) &
                                        (Donations.donation_amount == donation_amount))
            logger.info(donation_db)
            donation_db.delete_instance()
            #Donations.delete().where(Donations.donated_by_id == donor_name)
            logger.info(f'Deleted {donor_name} {donation_amount}from the database')

    except Exception as e:
        logger.info('Error deleting {} from database'.format(donor_name))
        logger.info(e)
    finally:
        logger.info('Closing delete_donation_from_db database connection')
        database.close()


def delete_donor_from_db(donor_name):
    """
    Removes this donor from the database. Also removes all the donors donations from the database as well 
    (can't leave orphan records!)
    """
    try:
        logger.info('Opening database connection to remove donor')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            logger.info(f'Deleting {donor_name} from Donations')
            donation_db = Donations.get(Donations.donated_by_id == donor_name)
            donation_db.delete_instance()
            #Donations.delete().where(Donations.donated_by_id == donor_name)

            logger.info(f'Deleting {donor_name} from Donors')
            donor_db = Donors.get(Donors.fullname == donor_name)
            donor_db.delete_instance()
            #Donors.delete().where(Donors.fullname == donor_name)
            logger.info(f'Deleted {donor_name} from the database')

    except Exception as e:
        logger.info('Error deleting {} from database'.format(donor_name))
        logger.info(e)
    finally:
        logger.info('Closing database connection for removing a donor')
        database.close()
