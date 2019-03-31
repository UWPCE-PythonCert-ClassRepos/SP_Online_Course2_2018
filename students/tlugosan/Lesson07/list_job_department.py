"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from persondepartmentjob_model import *
from datetime import datetime

import logging


def calculate_duration(start_date, end_date):
    ed = datetime.strptime(end_date, '%Y-%m-%d')
    st = datetime.strptime(start_date, '%Y-%m-%d')
    duration = (ed - st).days
    return duration


def join_classes():
    """
        demonstrate how to join classes together : no matches too
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('View any record of People that had a job and for how long')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job
                 .select(Job, Department)
                 .join(Department, JOIN.INNER)
                 )

        logger.info('View matching records from both tables')
        for job in query:
            logger.info(
                f'{job.person_employed} worked in {job.department_number.department_name} '
                f'for ' + str(calculate_duration(job.start_date,
                                                 job.end_date)) +
                f' days as '
                f'{job.job_name}')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    join_classes()
