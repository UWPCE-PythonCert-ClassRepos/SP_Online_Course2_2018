# ---------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: donor_class.py
# DATE CREATED: 11/18/2018
# UPDATED: 11/26/2018
# PURPOSE: Lesson 07 pt 2
# DESCRIPTION:  This file contains the set-up for the database (BaseModel, Meta, Donor, and
#               Donation classes to work behind-the-scenes for the SQLite-based database.
#               It also contains the pre-fabricated donors to add to the database when the
#               the program is first run.
# ---------------------------------------------------------------------------------------------
import logging
import datetime
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Defining the data (schema)')
database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        Donor class constraints
    """
    donor_name = CharField(primary_key=True, max_length=40)
    sum_all_donations = FloatField(null=True)
    count_all_donations = IntegerField(null=True)
    avg_all_donations = FloatField(null=True)


class Donation(BaseModel):
    """
        Donation class constraints
    """
    donor_name = ForeignKeyField(Donor, column_name='donor_name', null=False, on_delete='CASCADE')
    donation_amount = FloatField(null=False)


# Adding pre-fab donors to the db


if __name__ == '__main__':
    logger.info('Creating database...')
    try:
        database.create_tables([
            Donor,
            Donation])
    except Exception as e:
        logging.info(e)
    finally:
        database.close()
    logger.info('Adding pre-fab donors to database...')
    pre_fab = {
        'Harry Potter': [1000, 50],
        'Hermione Granger': [1000, 250, 1250],
        'Ron Weasley': [250],
        'Albus Dumbledore': [20000, 15000, 40000, 10000, 15000]
    }

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for key, val in pre_fab.items():
            with database.transaction():
                new_donor = Donor.create(
                    donor_name=key,
                    sum_all_donations=sum(val),
                    count_all_donations=len(val),
                    avg_all_donations=sum(val) / len(val),
                )
                new_donor.save()

                for amount in val:
                    new_donation = Donation.create(
                        donor_name=key,
                        donation_amount=amount
                    )
                    new_donation.save()

        for donor in Donor:
            logger.info('Donor, {}, has donated {} time(s) '
                        'the sum of all gifts donated is ${:,.2f}\n '
                        'with an average of {} per gift.'.format(donor.donor_name,
                                                                 donor.count_all_donations,
                                                                 donor.sum_all_donations,
                                                                 donor.avg_all_donations))
        for donation in Donation:
            logger.info('Donation value {:,.2f} successfully created for {}'.
                        format(donation.donation_amount,
                               donation.donor_name))
    except Exception as e:
        logger.info('Error while creating records. See error: {}'.format(donor.donor_name, e))
    finally:
        database.close()
