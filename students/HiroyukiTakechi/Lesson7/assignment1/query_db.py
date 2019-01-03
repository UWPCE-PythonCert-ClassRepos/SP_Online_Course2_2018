"""
    Assignment 1: Query the database table
    Finally, produce a list using pretty print that shows 
    all of the departments a person worked in for every job they ever had. 
"""

from create_db import *
from populate_db import *
import logging
import pprint

  
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
databse = SqliteDatabase('personjob.db')


def query_db():

    try:
        databse.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('produce a list using pretty print that shows all of the departments a person worked in for every job they ever had.')


        query = (Person
            .select(Person, Job, Department)
            .join(Job, JOIN.LEFT_OUTER, on = (Person.person_name 
                    == Job.person_employed_id))
            .join(Department, JOIN.LEFT_OUTER, on = (Job.department_id
                  == Department.department_id)))

        for person in query:

            pprint.pprint('Name: {}, Job Title: {}, Deparment: {}, Duration (Days): {}'.format(person.person_name, person.job.job_name, person.job.department_id, person.job.duration))


    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()        

if __name__ == '__main__':
    query_db()

