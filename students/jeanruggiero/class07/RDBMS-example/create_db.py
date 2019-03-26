"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *
from personjob_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_person(person):
    """
    Add a person to the job_history database.
    """

    database = SqliteDatabase('job_history.db')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    logger.info(f'Adding {person[PERSON_NAME]} to job_history.db')

    try:
        database.connect()
        with database.transaction():
            new_person = Person.create(
                    person_name=person[PERSON_NAME],
                    lives_in_town=person[LIVES_IN_TOWN],
                    nickname=person[NICKNAME])
            new_person.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)

    finally:
        logger.info('Close the database.')
        database.close()


def add_department(department):
    """
    Add a department to the job_history database.
    """

    database = SqliteDatabase('job_history.db')

    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    logger.info(f'Adding department {department[DEPARTMENT_NUMBER]} to job_history.db')

    try:
        database.connect()
        with database.transaction():
            new_dept = Department.create(
                    department_number=department[DEPARTMENT_NUMBER],
                    department_name=department[DEPARTMENT_NAME],
                    department_manager=department[DEPARTMENT_MANAGER])
            new_dept.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating department {department[DEPARTMENT_NUMBER]}')
        logger.info(e)

    finally:
        logger.info('Close the database.')
        database.close()


def add_job(job):
    """
    Add a job to the job_history database.
    """

    database = SqliteDatabase('job_history.db')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    JOB_DEPARTMENT = 5

    logger.info(f'Adding job {job[JOB_NAME]} to job_history.db')

    try:
        database.connect()
        with database.transaction():
            new_job = Job.create(
                job_name=job[JOB_NAME],
                start_date=job[START_DATE],
                end_date=job[END_DATE],
                salary=job[SALARY],
                person_employed=job[PERSON_EMPLOYED],
                job_department=job[JOB_DEPARTMENT])
            new_job.save()

    except Exception as e:
        logger.info(f'Error creating job {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def print_jobs():
    """
    Pretty print all of the jobs held by each person and their departments.
    :return: None
    """

    logger.info("Preparing to pretty print each person's job and corresponding department.")
    database = SqliteDatabase('job_history.db')
    database.connect()

    query = (Person
             .select(Person, Job)
             .join(Job, JOIN.INNER)
             .join(Department, JOIN.INNER)
             )

    for p in query:
        print(f'{p.person_name} had job {p.job.job_name} in department {p.job.job_department.department_name} for {p.job.job_length} days.')


if __name__ == '__main__':

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
        ('Pam', 'Coventry', 'PJ'),
        ('Steven', 'Colchester', None),
        ]

    departments = [
        ('Ab34', 'Marketing', 'Joe'),
        ('a456', 'Sales', 'Mary'),
        ('7892abg', 'Wrong dept code', 'Bob'),
        ('8agb', 'Also wrong', 'BillyBob')
        ]

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'Ab34'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'Ab34'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'Ab34'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'a456'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'a456')
        ]

    for person in people:
        add_person(person)

    for department in departments:
        add_department(department)

    for job in jobs:
        add_job(job)

    print_jobs()



