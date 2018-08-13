"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from create_database import *
from datetime import datetime, timedelta
from dateutil.parser import parse
import pprint

import logging

def date_converter(date):
    return datetime.strptime(''.join(date.split('-')), '%Y%m%d')

def dates_diff(date2, date1):
    return (date_converter(date2)-date_converter(date1)).days

def populate_persons():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personnel_database.db')

    logger.info('Working with Person class')

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

    finally:
        logger.info('database closes')
        database.close()

def populate_depts():
    """
    add departments data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personnel_database.db')

    logger.info('Working with Department class')

    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MGR = 2

    depts = [
        ('ASYS', 'Analyst', 'Ryan Howard'),
        ('ADMN', 'Administration', 'Pamela Halpert'),
        ('BUSI', 'Business', 'Angela Martin')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in depts:
            with database.transaction():
                new_department = Department.create(
                    department_number = dept[DEPT_NUM],
                    department_name = dept[DEPT_NAME],
                    department_manager = dept[DEPT_MGR],)
                new_department.save()

        logger.info('Print the Department records we saved...')
        for dept in Department:
            logger.info(f'{dept.department_number} : {dept.department_manager} ' +\
                        f'manages {dept.department_name}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_jobs():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personnel_database.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'ASYS'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'ASYS'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'BUSI'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'ADMN'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'ADMN')
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
                    duration = dates_diff(job[END_DATE], job[START_DATE]),
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_department = job[DEPARTMENT])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed} in {job.job_department}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    populate_persons()
    populate_depts()
    populate_jobs()
