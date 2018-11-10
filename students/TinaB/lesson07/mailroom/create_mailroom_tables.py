"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we create the tables from our model
"""

import logging
from peewee import *
from  mailroom_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('donor_database.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

logger.info('Adding tables to database')
# try:
#logger.info('dropping table and creating tables')
# database.drop_tables([Donors, Donations])  # dropping if exists
#database.create_tables([Donors, Donations])
# except Exception as e:
#    raise e
database.create_tables([Donors, Donations])
logger.info('Database tables created successfully')
database.close()
