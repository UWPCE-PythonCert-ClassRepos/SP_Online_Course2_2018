import logging
from peewee import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donors.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

class BaseModel(Model):
    class Meta:
        database = database

class Donorinfo(BaseModel):

    logger.info('Creating Donor class.')
    donor_name = CharField(primary_key=True,max_length = 30, null=False)
    sum_donations = FloatField()
    number_donations = IntegerField()
    avg_donations = FloatField()

class Donationinfo(BaseModel):

    donation_amount = FloatField()
    donor_name = ForeignKeyField(Donorinfo, related_name='donated by')



database.create_tables([
        Donorinfo,
        Donationinfo
    ])

database.close()

def populate_donors(donors):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('donors.db')

    logger.info('Working with Donor class')


    try:
        for donor, amount in donors.items():
            new_donor = Donorinfo.create(
                donor_name = donor,
                sum_donations = sum(amount),
                number_donations = len(amount),
                avg_donations = sum(amount)/len(amount))
            new_donor.save()
            logger.info('Database add successful.')
        for donor, amount in donors.items():
            for gift in amount:
                new_gift = Donationinfo.create(
                donation_amount = gift,
                donor_name = donor
                )
                new_gift.save()
                logger.info('Giftinfo add successful')


    except Exception as e:
        logger.info(f'Unable to add donor to database.')
        logger.info(e)

    finally:
        logger.info('Closing database.')
        database.close()

if __name__ == "__main__":
    donors = {"Andy": [960, 256, 123.5, 40],"Bryce": [30, 45, 27],"Charile": [25, 50],"David": [10],"Elaine": [75, 26]}
    populate_donors(donors)
