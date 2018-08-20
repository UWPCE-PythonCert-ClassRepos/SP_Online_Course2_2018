"""
Generating people, jobs, and departments from the personjob model
"""

from personjob_model import *
import logging
from pprint import pprint

def populate_db():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2
    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
    ]

    database = SqliteDatabase('personjob.db')

    logger.info('Populating database with person records')
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in people:
            with database.transaction():
                new_person = Person.create(
                    person_name = person[PERSON_NAME],
                    lives_in_town = person[LIVES_IN_TOWN],
                    nickname = person[NICKNAME])
                new_person.save()
                logger.info('Successfully added person')
    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)

    logger.info('Now populating database with job records')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT_NUMBER = 5
    DURATION = 6

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'A201', 1.4),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'A401', 3.6),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'A101', 10.1),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter', 'A301', 2.1),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'A201', 3.3),
        ('Programmer', '2016-01-01', '2017-01-05', 70000, 'Susan', 'A101', 1),
        ('Senior programmer', '2017-01-05', '2018-01-05', 90000, 'Susan', 'A301', 1)
        ]

    try:
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    department_number = job[DEPARTMENT_NUMBER],
                    duration = job[DURATION])
                new_job.save()
                logger.info('Successfully added job')
    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    logging.info('Now populating department info')

    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    departments = [
        ('A101', 'IT', 'George Kritsonis'),
        ('A201', 'Manufacturing', 'Dave Walter'),
        ('A301', 'Supply chain', 'Michael Rojas'),
        ('A401', 'HR', 'Greena George')
    ]

    try:
        for department in departments:
            with database.transaction():
                new_dept = Department.create(
                    department_number = department[DEPARTMENT_NUMBER],
                    department_name = department[DEPARTMENT_NAME],
                    department_manager = department[DEPARTMENT_MANAGER])
                new_dept.save()
                logger.info('Successfully created new department record')
    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_NUMBER]}')
        logger.info(e)

def pretty_print_data():
    try:
        database = SqliteDatabase('personjob.db')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys=ON;')
        query = (Person
            .select(Person, Job, Department)
            .join(Job, JOIN.LEFT_OUTER)
            .join(Department, JOIN.LEFT_OUTER, on = (Job.department_number
                  == Department.department_number)))
        for person in query:
            pprint(f'{person.person_name} had job {person.job.job_name} '\
                f'in the {person.job.department.department_name} department')
    except Exception as e:
        logging.info(e)

if __name__ == '__main__':
    populate_db()
    pretty_print_data()
