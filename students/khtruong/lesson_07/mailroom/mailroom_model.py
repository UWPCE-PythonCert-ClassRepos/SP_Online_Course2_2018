"""Mailroom Model"""
import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donation.db')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    name = CharField(primary_key=True, max_length=30, null=False)
    avg_donation = FloatField()
    total_donation = FloatField()
    num_donations = IntegerField()


class Donation(BaseModel):
    amount = DecimalField(null=False)
    donor = ForeignKeyField(Donor, null=False)


if __name__ == "__main__":
    logger.info('create database')
    try:
        database.create_tables([Donor, Donation])
    except Exception as e:
        logging.info(e)
    finally:
        database.close()

    logger.info('Populate database')
    db = {
        'Jeff Bezos': [3.65, 54.50],
        'Mark Zuckerberg': [36.54, 1.25, 54.87],
        'Paul Allen': [17.38],
        'William Gates': [25.55, 33.33, 78.14]
    }

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for key, val in db.items():
            with database.transaction():
                donor = Donor.create(
                    name=key,
                    avg_donation=sum(val) / len(val),
                    total_donation=sum(val),
                    num_donations=len(val)
                )
                donor.save()

                for d in val:
                    donation = Donation.create(
                        amount=d,
                        donor=key
                    )
                donation.save()

        for donor in Donor:
            logger.info(f'{donor.name}, '
                        f'{donor.avg_donation}, '
                        f'{donor.total_donation}, '
                        f'{donor.num_donations}')

        for donation in Donation:
            logger.info(f'{donation.donor}, '
                        f'{donation.amount}')

    except Exception as e:
        logger.info(e)
    finally:
        database.close()
