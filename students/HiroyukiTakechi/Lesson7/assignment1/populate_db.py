"""
   Assignment 1: populate the database table
"""

import logging
from create_db import *

def populate_db_person():
    """
        populate person database table
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
        ('Steven', 'Colchester', None)]

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
        for person in Person:
            logger.info(f'{person.person_name} lives in {person.lives_in_town} ' +\
                f'and likes to be known as {person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def populate_db_job():
    """
        populate job database table
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
    DEPARTMENT_ID = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew','A123'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'B123'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'C123'),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter','D123'),
        ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter', 'E123')
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
                    department_id = job[DEPARTMENT_ID])

                new_job.save()
                logger.info('Database add successful')

        logger.info('Print the Job records we saved...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')


    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

def populate_db_department():
    """
        populate department database table
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Department class')
    logger.info('Creating Department records: just like Person. We use the foreign key')

    DEPARTMENT_ID = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2
    #START_DATE_DEPARTMENT = 3
    #END_DATE_DEPARTMENT = 4
    #DURATION = 5
  

    departments = [
        ('A123', 'Operations', 'Andrew'),
        ('B123', 'Marketing', 'Peter'),
        ('C123', 'Finance', 'Susan'),
        ('D123', 'HR', 'Pam'),
        ('E123', 'Sales', 'Steven')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    department_ID = department[DEPARTMENT_ID],
                    department_name = department[DEPARTMENT_NAME],
                    department_manager = department[DEPARTMENT_MANAGER])

                new_department.save()
                logger.info('Database add successful')

        logger.info('Print the Department records we saved...')
        for department in Department:
            logger.info(f'{department.department_id} is {department.department_name} ' +\
                f'and the manager is {department.department_manager}')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    populate_db_person()
    populate_db_job()
    populate_db_department()
