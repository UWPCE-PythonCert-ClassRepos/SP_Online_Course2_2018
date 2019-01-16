import logging

from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') 


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('Checkpoint: Change Donor info')

    donor_name = CharField(max_length = 40)
    donor_id = CharField(primary_key = True, max_length = 30)
    
    logger.info('Checkpoint: Donor info modified.')


class Donation(BaseModel):
    """
    """
    logger.info('Checkpoint: Donation added')
    
    amount = DecimalField(max_digits = 15, decimal_places = 2)
    donation_id = IntegerField()
    donated_by = ForeignKeyField(Donor, related_name='was_offered_by', null = False)
    
    logger.info('Checkpoint: Donation info modified')

if __name__ == '__main__':
    database.create_tables([
            Donor,
            Donation
        ])

    database.close()
