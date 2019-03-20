"""
File Name: donor_report.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 3/19/2019
Python Version: 3.7.0
"""

import logging
import datetime
from peewee import fn, SqliteDatabase
from donordb_model import Donor, Donation
database = SqliteDatabase('donation_tracker.db')


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def list_by_total():
    try:
        database.connect()
        query = (Donor
               .select(Donor.name,
                       fn.SUM(Donation.donation_amount).alias('total_donations'),
                       fn.COUNT(Donation.donation_amount).alias('count'),
                       (fn.AVG(Donation.donation_amount).alias('avg'))
                       )
               .join(Donation)
               .group_by(Donor.name)
               .order_by(fn.SUM(Donation.donation_amount).desc())
               )
        return tuple([(d.name,
                      d.total_donations,
                      d.count,
                      d.avg)
                      for d in query])
    except Exception as e:
        log.info(e)
    finally:
        database.close()

def print_report():
    """Prints report of all donors"""
    categories = ['Donor Name', 'Total Given', 'Num Gifts', 'Average Gift']
    spacing = "{:<20} $ {:>10.2f} {:>10}     $ {:>10.2f}\n"
    sorted_tuple = list_by_total()
    header = "{:<20}| {:>10} | {:>10} | {:>10}\n"
    print(header.format(*categories))
    for donor in sorted_tuple:
        print(spacing.format(donor[0], donor[1], donor[2], donor[3]))

print_report()
