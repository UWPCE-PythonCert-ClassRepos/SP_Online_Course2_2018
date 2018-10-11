"""
    This module sets up tables
"""

import logging
from peewee import *  # noqa F403
from models import *  # noqa F403

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('mailroom.db')  # noqa F403

try:
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    database.create_tables([
        Donor,  # noqa F403
        Donation  # noqa F403
    ])
    logger.info('Tables created.')
except Exception as e:
    logger.info(e)
finally:
    database.close()  # noqa F403
