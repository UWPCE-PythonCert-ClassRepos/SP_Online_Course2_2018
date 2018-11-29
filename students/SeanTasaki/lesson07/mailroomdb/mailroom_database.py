

import logging
from peewee import *  
from mailroomdb_queries import PeeweeDBConnection


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')


class BaseModel(Model):  
    class Meta:
        database = database


class Donor(BaseModel):
    donor_id= AutoField()
    first_name = CharField(max_length=30)  
    last_name = CharField(max_length=30)  


class Donation(BaseModel):
    donation = FloatField()  
    donor = ForeignKeyField(Donor, column_name='donor_id')


dbconnection = PeeweeDBConnection(database)

with dbconnection as db:

    if Donor.table_exists():
        Donation.drop_table()
        Donor.drop_table()
        
    
    database.create_tables({Donor, Donation})
    logger.info('Tables created')
