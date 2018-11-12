"""
    This program prints the person, job, and department tables
"""

from pprint import pprint as pp
from create_personjobdept import *
import logging


def printdb():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job.select())
        pp('Job Name                  | Employee        | Department     ')
        pp('-------------------------------------------------------------')
        for job in query:
            pp('{:25} | {:15} | {:15}'.format(
                job.job_name, str(job.person_employed), job.department_name))
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    printdb()
