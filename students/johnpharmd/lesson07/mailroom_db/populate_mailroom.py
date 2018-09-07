import logging
from peewee import SqliteDatabase
from peewee import Model
from peewee import CharField
from peewee import IntegerField
import mailroom_model


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in ' +
            'the database')

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor instances, each of which maintains
        details of an individual donor.
    """
    title = CharField(max_length=10)
    last_name = CharField(primary_key=True, max_length=30)
    total_donation_amt = IntegerField()
    num_donations = IntegerField()


def populate_db():
    """
        Add data for each donor to database.
    """
    logger.info('Working with Donor class')

    TITLE = 0
    LAST_NAME = 1
    TOTAL_DONATION_AMT = 2
    NUM_DONATIONS = 3

    donors = [
        ('Mr.', 'Gates', 150000, 3),
        ('Mr.', 'Brin', 150000, 3),
        ('Mr.', 'Cerf', 50000, 2),
        ('Mr.', 'Musk', 100000, 1),
        ('Mr.', 'Berners-Lee', 50000, 2),
        ('Ms.', 'Wojcicki', 125000, 1),
        ('Ms.', 'Avey', 200000, 2)
        ]

    try:
        for donor in donors:
            with database.transaction():
                new_donor = Donor.create(
                        title=donor[TITLE],
                        last_name=donor[LAST_NAME],
                        total_donation_amt=donor[TOTAL_DONATION_AMT],
                        num_donations=donor[NUM_DONATIONS])
                new_donor.save()
                logger.info('Database add successful')

        logger.info('Print the Donor records we saved...')
        for saved_donor in Donor:
            logger.info(f'{saved_donor.title} ' +
                        f'{saved_donor.last_name} ' +
                        f'has donated {saved_donor.total_donation_amt}')

    except Exception as e:
        logger.info(f'Error creating = {donor[LAST_NAME]}')
        logger.info(e)


database.create_tables([Donor])

if __name__ == '__main__':
    populate_db()
    database.close()
