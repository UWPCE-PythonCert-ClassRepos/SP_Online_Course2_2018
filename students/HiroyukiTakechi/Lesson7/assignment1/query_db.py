"""
    Assignment 1: Query the database table
"""

from create_db import *
import logging
import pprint

    
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

databse = SqliteDatabase('personjob.db')

logger.info('Showing all of the departments a person worked in for every job they ever had')

def query_db():

    try:
        databse.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (Department
                 .select(Department, Job)
                 .join(Job, JOIN.LEFT_OUTER)
                 .group_by(job.person_employed))

        for department in query:
            pprint.pprint('{}, {}, {}'.format(department.department_name, job.job_name, job.person_employed))


    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closes')
        dabase.close()        

if __name__ == '__main__':
    query_db()
    
















