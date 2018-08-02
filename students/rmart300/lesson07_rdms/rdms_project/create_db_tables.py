"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *
import personjob_model as db_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

database.create_tables([
        db_model.Department,
        db_model.Job,
        db_model.Person 
    ])

logger.info('Database tables created successful')

database.close()

