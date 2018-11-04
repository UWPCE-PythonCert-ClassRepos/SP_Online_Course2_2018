"""
Final Part for lesson 07 assignment one
Finally, produce a list using pretty print that shows all of 
the departments a person worked in for every job they ever had.
"""

from pprint import pprint as pp
from personjobdept_model import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjobdept.db')


def print_personjobdept():
    """
    Prints a all the deptments that a person has worked for for evey job
    Needs to connect the three database tables person, job, department
    """

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for job in Job:
            pp(f'{job.person_employed.person_name} was a(n) {job.job_name} in the'
               + f' {job.job_department.department_name} department')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    print_personjobdept()
