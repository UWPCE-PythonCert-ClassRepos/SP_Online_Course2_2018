import pprint
from peewee import *
from create_db import *
import logging

def print_jobs():
    """
        Print all the jobs along with the relevant employee and department
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    pp = pprint.PrettyPrinter(indent=2)

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = Job.select(Job, Person, Department).join(Person).switch(Job).join(Department)
        for job in Job:
            try:
                pp.pprint(f'Person {job.person_employed.person_name} had job {job.job_name} in department {job.department_employed.department_name} for {job.duration} days')
            except Exception as e:
                logger.info(e)
    except Exception as e:
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    print_jobs()