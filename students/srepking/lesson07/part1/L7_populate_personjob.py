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


def populate_departments():
    """
    Add department data to database with columns Department Number,
    Department Name, Department Manager, Job Name, and Total Days
    position was held.
    """
    DEPT_number = 0
    DEPT_name = 1
    DEPT_manager = 2

    logger.info('Starting to load deparatment data.')

    department_data = [
        ('C191', 'Operations', 'Dick'),
        ('C291', 'Transmission', 'Mary'),
        ('C391', 'Generation', 'Pat'),
        ('C491', 'HumanResources', 'Rob'),
        ('C591', 'Distribution', 'Cindy')
        ]

    try:
        for departs in department_data:
            with database.transaction():
                new_dept = Department.create(
                    dept_number=departs[DEPT_number],
                    dept_name=departs[DEPT_name],
                    dept_manager=departs[DEPT_manager]
                    )
                new_dept.save()

    finally:
        logger.info('finished loading department data.')



def populate_jobs():
    """
    Add jobs data to database.
    """
    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT_NUMBER = 5

    logger.info('Starting to load jobs')

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'C191'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'C191'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000,
         'Andrew', 'C191'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'C291'),
        ('CEO', '2014-11-14', '2018-01-05', 45900, 'Peter', 'C291')
        ]

    try:
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    salary=job[SALARY],
                    days_held = None,
                    person_employed=job[PERSON_EMPLOYED],
                    dept_num=job[DEPT_NUMBER])
                new_job.save()

# Calculate days help in a position from the data in the tables
        for job in Job:
            with database.transaction():
                date_format = "%Y-%m-%d"
                # Get start_date and end_date from Job Table and parse
                # date string into python format
                startday = datetime.strptime(job.start_date, date_format)
                endday = datetime.strptime(job.end_date, date_format)
                totaldays = (endday - startday).days  # returning the days only
                job.days_held = totaldays
                job.save()
# Print how long each person worked in their job.

        for job in Job:
            logger.info(f'{job.person_employed} worked as '
                        f'{job.job_name} for {job.days_held} days.')

    finally:
        logger.info('finished loading jobs')


def join_classes():
    """
        Create a list of every department each person worked for.
        Joins the Person table to Job table, and then those results get joined
        to the Department table.
    """

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        # #######################################################
        # Getting this error for this
        # query. 'Job' object has no attribute 'department'
        # #############################################3

        query = (Job
                 .select(Job, Department.dept_name)
                 .join(Department, JOIN.INNER))  # Joins Job -> Department

        query_tuple = []  # Create a list to hold person, job, and dept.
        for job in query:
            query_tuple.append((job.person_employed, job.job_name,
                                job.department.dept_name))

        return query_tuple

    except Exception as e:
        logger.info(f'Error creating query')
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
    populate_departments()
    populate_jobs()
    database.close()
    logger.info('Call join_classes and print the person, '
                'their job, and the department they were in.')
    pprint.pprint(join_classes())
