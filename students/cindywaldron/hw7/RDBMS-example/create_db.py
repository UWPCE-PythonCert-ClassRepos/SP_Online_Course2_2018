#!/usr/bin/env python3

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
import pprint
from create_personjob import *

def populate_people():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Person class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for this from a user')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
        ('Pam', 'Coventry', 'PJ'),
        ('Steven', 'Colchester', None),
        ]

    logger.info('Creating Person records: iterate through the list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

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
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def populate_jobs():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    JOB_DURATION = 5
    JOB_DEPARTMENT = 6

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 100, 'A123'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Susan', 250, 'H987'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 200, 'P345'),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter', 450, 'S999'),
        ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter', 300, 'L888')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_duration = job[JOB_DURATION],
                    job_department = job[JOB_DEPARTMENT])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

def populate_departments():
    """
        add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Department class')
    logger.info('Creating department records:')

    DEPARTMENT_NUM = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MGR = 2


    departments = [
        ('A123', 'Agriculture', 'John Doe'),
        ('H987', 'Housing', 'Margret Bay'),
        ('P345', 'Police', 'Bart Simpson'),
        ('S999', 'Security', 'Mike Bennet'),
        ('L888', 'Licensing', 'Sam Johnson')
        ]

    try:
        database.connect()
        #database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    department_number = department[DEPARTMENT_NUM],
                    department_name = department[DEPARTMENT_NAME],
                    department_manager = department[DEPARTMENT_MGR])

                new_department.save()

        logger.info('Reading and print all Department rows ...')
        for department in Department:
            logger.info(f'{department.department_number} : {department.department_name} Manager is {department.department_manager}')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_NUM]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

def display_people():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Find and display a list of people worked in the departments...')

        query = (Job
                 .select(Job, Person, Department)
                 .join(Person)
                 .switch(Job)
                 .join(Department)
                )

        for job in query:
            try:
                pp = pprint.PrettyPrinter(depth=3)
                row = "Person Name: " + job.person_employed.person_name \
                        + "      Job: " + job.job_name \
                        + "      Department: " + job.job_department.department_name
                pp.pprint(row)

            except Exception as e:
                print(e)
                logger.info(f'Person {job.person_employed.person_name} had no job')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    populate_departments()
    populate_people()
    populate_jobs()
    display_people()