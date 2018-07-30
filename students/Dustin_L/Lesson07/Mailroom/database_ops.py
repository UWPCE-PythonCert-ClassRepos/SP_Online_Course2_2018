#!/usr/bin/env python3
"""This module contains all of the database specific operations for the
    Peewee Database Mail Room
"""
import decimal
import logging
import peewee as pw
import donor_database_model as dm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_donor_names(donor_db):
    """Generator yielding all Donor names as strings from passed database

    Args:
        donor_db (SqliteDatabase): SqliteDatabase
    """
    with donor_db as db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        donor_names = dm.Donor.select(dm.Donor.name)
        for name in donor_names:
            yield str(name)


def add_donor(name_add, donor_db):
    """Adds name Donor to database without any donation history.

    If donor already exists in the database, no duplicate is added.

    Args:
        name_add (str): Name of new donor.
        donor_db (SqliteDatabase): SqliteDatabase.
    """
    with donor_db as db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        try:
            dm.Donor.create(name=name_add.title(),
                            total_donations=0,
                            ave_donations=0)
        except pw.IntegrityError:
            logger.info(f'Attempted to add a donor already in the database: '
                        f'{name_add}')


def add_donation(donor, donation, donor_db):
    """Adds Donation to database and updates appropriate Donor information.

    Args:
        donor (str): name of Donor.
        donation (float): Donation amount.
        donor_db (SqliteDatabase): SqliteDatabase.
    """
    with donor_db as db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        dm.Donation.create(donor_name=donor,
                           amount=donation)

        d = dm.Donor().get(dm.Donor.name == donor)
        d.total_donations = d.total_donations + decimal.Decimal(donation)
        d.ave_donations = d.total_donations / len(d.donations)
        d.save()


def update_donation(donor, donation, new_donation, donor_db):
    """Updates a donation based on donor name and donation amount.

    Args:
        donor (str): donor name
        donation (float): donation to match
        donor_db (SqliteDatabase): SqliteDatabase.
    """
    with donor_db as db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        query = dm.Donation.select().where((dm.Donation.donor_name == donor) &
                                           (dm.Donation.amount == float(donation)))
        for match in query:
            match.amount = new_donation
            match.save()

            d = dm.Donor().get(dm.Donor.name == donor)
            total = 0
            for dn in d.donations:
                total = total + dn.amount
            d.total_donations = total
            d.ave_donations = d.total_donations / len(d.donations)
            d.save()


def delete_donor(donor, donor_db):
    """Delete the specified donor and all of their respective donations from
       the database.

    Args:
        donor (str): donor name.
        donor_db (SqliteDatabase): SqliteDatabase
    """
    with donor_db as db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        query = dm.Donor.select().where(dm.Donor.name == donor)
        for match in query:
            for donation in match.donations:
                donation.delete_instance()

            match.delete_instance()
