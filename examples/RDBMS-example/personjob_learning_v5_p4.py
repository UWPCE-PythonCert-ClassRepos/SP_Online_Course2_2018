"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from personjob_model import *

import logging

def show_integrity_add():
    """
        demonstrate how database protects data inegrity : add
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            logger.info('Try to add a new job where a person doesnt exist...')

            addjob = ('Sales', '2010-04-01', '2018-02-08', 80400, 'Harry')

            logger.info('Adding a sales job for Harry')
            logger.info(addjob)
            new_job = Job.create(
                job_name = addjob[JOB_NAME],
                start_date = addjob[START_DATE],
                end_date = addjob[END_DATE],
                salary = addjob[SALARY],
                person_employed = addjob[PERSON_EMPLOYED])
            new_job.save()

    except Exception as e:
        logger.info('Add failed because Harry is not in Person')
        logger.info(f'For Job create: {addjob[0]}')
        logger.info(e)

if __name__ == '__main__':
    show_integrity_add()
