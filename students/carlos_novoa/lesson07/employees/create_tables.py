"""
    This module sets up tables
"""

import logging
from peewee import *  # noqa F403
from models import *  # noqa F403

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    database = SqliteDatabase('staff.db')  # noqa F403
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
    database.create_tables([
        Person,  # noqa F403
        Job,  # noqa F403
        Department  # noqa F403
    ])
    logger.info('Tables created')

except Exception as e:
    logger.info(e)

finally:
    database.close()
