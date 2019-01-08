# ------------------------------------------------- #
# Title: Lesson 7, Database Management, Mail Room
# Dev:   Craig Morton
# Date:  12/20/2018
# Change Log: CraigM, 1/2/2019, Database Management, Mail Room
# ------------------------------------------------- #

# populate database

import logging
import datetime
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Defining Schema')

database = SqliteDatabase('mailroom.db')
database.connect()


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """Donor class constraints"""
    donor_name = CharField(primary_key=True, max_length=40)
    sum_all_donations = FloatField(null=True)
    count_all_donations = IntegerField(null=True)
    avg_all_donations = FloatField(null=True)


class Donation(BaseModel):
    """Donation class constraints"""
    donor_name = ForeignKeyField(Donor, null=False, related_name='was_filled_by')
    donation_amount = FloatField(null=False)


if __name__ == '__main__':
    logger.info('Creating database')
    try:
        database.create_tables([
            Donor,
            Donation])
    except Exception as e:
        logging.info(e)
    finally:
        database.close()
    logger.info('Adding existing donors to database')
    pre_fab = {
        'Bill Gates': [1400, 5050, 213],
        'Nikola Tesla': [43298, 3490, 2390],
        'Elon Musk': [3094],
        'Linus Torvalds': [23942, 12394, 594, 10, 239]}

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for key, val in pre_fab.items():
            with database.transaction():
                new_donor = Donor.create(
                    donor_name=key,
                    sum_all_donations=sum(val),
                    count_all_donations=len(val),
                    avg_all_donations=sum(val) / len(val))
                new_donor.save()
                for amount in val:
                    new_donation = Donation.create(
                        donor_name=key,
                        donation_amount=amount)
                    new_donation.save()

        for donor in Donor:
            logger.info('Donor, {}, has donated {} time(s) '
                        'the total of all donations is ${:,.2f}\n '
                        'with an average of {} per gift.'.format(donor.donor_name,
                                                                 donor.count_all_donations,
                                                                 donor.sum_all_donations,
                                                                 donor.avg_all_donations))
        for donation in Donation:
            logger.info('Donation value {:,.2f} successfully created for {}'.
                        format(donation.donation_amount,
                               donation.donor_name))
    except Exception as e:
        logger.info('Record creation error!: {}'.format(donor.donor_name, e))
    finally:
        database.close()
