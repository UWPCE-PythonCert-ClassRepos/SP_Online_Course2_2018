from datetime import datetime
from create_personjobdepartment import *

import logging

def days_between(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return abs((end_date - start_date).days)

def convert_datetime(end_date_in, start_date_in):
    end_date = str(end_date_in)
    start_date = str(start_date_in)
    return datetime.strptime(''.join(end_date.split('-')), '%Y%m%d') - datetime.strptime(''.join(start_date.split('-')), '%Y%m%d')

def join_classes():
    """
        demonstrate how to join classes together : no matches too
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_department.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job
                 .select(Job, Department)
                 .join(Department, JOIN.INNER)
                )

        for job in query:
            try:
                logger.info(f'{job.person_employed} held position \'{job.job_name}\' '\
                            f'in department {job.department.department_name} '\
                            f'for {days_between(job.start_date, job.end_date)} days')

            except Exception as e:
                logger.info(f'Person {job.person_employed} had no job')


    except Exception as e:
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    join_classes()
