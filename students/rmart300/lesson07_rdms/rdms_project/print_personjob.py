"""
produce a list using pretty print that shows all of the departments a person worked in for every job they ever had
"""

from personjob_model import *

import logging
import pprint

def print_personjob_records():
    """
        join classes together to print all jobs a person worked
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for job in Job:
            pprint.pprint(f'{job.person_employed.person_name} had job as {job.job_name} in department {job.job_department.department_name}')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    print_personjob_records()
