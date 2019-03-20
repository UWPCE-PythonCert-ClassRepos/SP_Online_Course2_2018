"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('maildonor.db', pragmas={'foreign_keys': 1})
database.connect()
#database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

logger.info('Creating the Classes from the base class')


class BaseModel(Model):
    """ Base class for peewee tables"""
    class Meta:
        database = database


class Donors(BaseModel):
    """
        Defines Donors
    """
    donor_name = CharField(primary_key = True, max_length = 30)
    lastname = CharField(max_length=30,  null = True)
    firstname = CharField(max_length=30,  null = True)

    logger.info('creating donors class')

class Donations(BaseModel):
    """
        Defines donations from donors
    """
    donor_key = ForeignKeyField(Donors, field="donor_name", backref='donations'
                                , null=False)
    amount = FloatField(default=0)
    date = DateField(formats= "%Y-%m-%d")

    class Meta:
        """creating our unique identifier for this table"""
        indexes = (
                   (('donor_key', 'amount'
                     ), True),
                   )


    logger.info('creating donation class')

database.create_tables([Donors, Donations])
logger.info('Database tables created successfully')
database.close()
