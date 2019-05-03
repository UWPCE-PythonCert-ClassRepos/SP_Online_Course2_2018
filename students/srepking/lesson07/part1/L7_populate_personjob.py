"""
    Loads the database that includes Department for assignment 7. You need
    to delete the database personjob.db before you run this.
"""

import logging
from L7_create_personjob import *
from peewee import *
import pprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from datetime import datetime


def populate_people():
    """
    add person data to database
    """

    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger(__name__)
    logger.info('Starting to load people')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
        ('Pam', 'Coventry', 'PJ'),
        ('Steven', 'Colchester', None)
        ]

    try:
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name=person[PERSON_NAME],
                        lives_in_town=person[LIVES_IN_TOWN],
                        nickname=person[NICKNAME])
                new_person.save()
                logger.debug('People data add successful')

        logger.debug('Print the Person records we saved...')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)

    finally:
        logger.info('finished loading people')


def populate_jobs():
    """
    Add jobs data to database.
    """
    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4

    logger.info('Starting to load jobs')

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000,
         'Andrew'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter'),
        ('CEO', '2014-11-14', '2018-01-05', 45900, 'Peter')
        ]

    try:
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED])
                new_job.save()

    finally:
        logger.info('finished loading jobs')


def populate_departments():
    """
    Add department data to database with columns Department Number,
    Department Name, Department Manager, Job Name, and Total Days
    position was held.
    """
    DEPT_number = 0
    DEPT_name = 1
    DEPT_manager = 2
    JOB_name = 3

    logger.info('Starting to load deparatment data.')

    department_data = [
        ('C191', 'Operations', 'Dick', 'Analyst'),
        ('C191', 'Transmission', 'Mary', 'Senior analyst'),
        ('C291', 'Generation', 'Pat', 'Senior business analyst'),
        ('C291', 'Operations', 'Rob',  'Admin supervisor'),
        ('C391', 'Distribution', 'Cindy', 'CEO')
        ]

    try:
        for Departments in department_data:
            with database.transaction():
                jobrow = Job.get(Job.job_name == Departments[JOB_name])
                date_format = "%Y-%m-%d"
                # Get start_date and end_date from Job Table and parse
                # date string into python format
                startday = datetime.strptime(jobrow.start_date, date_format)
                endday = datetime.strptime(jobrow.end_date, date_format)
                totaldays = (endday - startday).days  # returning the days only
                new_job = Department.create(
                    dept_number=Departments[DEPT_number],
                    dept_name=Departments[DEPT_name],
                    dept_manager=Departments[DEPT_manager],
                    job_name=Departments[JOB_name],
                    days_held=totaldays
                    )
                new_job.save()

    finally:
        logger.info('finished loading department data.')


def join_classes():
    """
        Joins the Person table to Job table, and then those results get joined
        to the Department table.
    """

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                 .select(Person, Job.job_name, Department.dept_name)
                 .join(Job, JOIN.INNER)  # Joins person - > Job
                 .join(Department, JOIN.INNER))  # Joins Job -> Department

        query_tuple = []  # Create a list to hold person, job, and dept.
        for person in query:
            query_tuple.append((person.person_name, person.job.job_name,
                                person.job.department.dept_name))
        return query_tuple

    except Exception as e:
        logger.info(f'Error creating')
        logger.info(e)

    finally:
        logger.info('database closes after join_classes')
        database.close()


if __name__ == '__main__':
    logger.info('Creating the Database.')
    database = SqliteDatabase('personjob.db')
    database.create_tables([
        Job,
        Person,
        PersonNumKey,
        Department
    ])

    database.connect()
    logger.info('database connects')
    database.execute_sql('PRAGMA foreign_keys = ON;')
    populate_people()
    populate_jobs()
    populate_departments()
    database.close()
    logger.info('Call join_classes and print the person, '
                'their job, and the department they were in.')
    pprint.pprint(join_classes())
