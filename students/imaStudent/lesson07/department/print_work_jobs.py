"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from work_db_model import *

import logging

def list_jobs():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('work.db')

    logger.info('Working with Job class')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job.select(Job.person_employed,
                            Job.job_name,
                            Job.dept_name)
            .order_by(Job.start_date))

        for job in query:
            logger.info(f'Person {job.person_employed} had job {job.job_name}')

    except Exception as e:
        logger.info('Error')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    list_jobs()

