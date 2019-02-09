"""
    Lesson 07 assignment
    Add department to personjob examples from class material
    starts with no database
"""

from personjob_model import *


import logging
import os
from datetime import datetime


def duration(d0, d1):
    """
    take dates as strings of format 'YYYY-MM-DD'
    return integer number of days between two dates
    always return positive number regardless of order of args
    """
    date_format = '%Y-%m-%d'
    date0 = datetime.strptime(d0, date_format)
    date1 = datetime.strptime(d1, date_format)
    return int(abs((date0 - date1).days))


def populate_persondata():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

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


def populate_jobdata():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT_NUMBER = 5
    DEPT_NAME = 6
    DEPT_MANAGER = 7

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'D123',
         'Thermal Engineering', 'Corey Frasier'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'M456',
         'Mechanical Design', 'Dan Carter'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew',
         'J789', 'War Room', 'Barath Kanagal'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'Y189',
         'Data Center Design', 'Suzy Jewett'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'Y189',
         'Data Center Design', 'Vik Tymchenko')
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
                    department_number = job[DEPT_NUMBER],
                    department_name = job[DEPT_NAME],
                    department_manager = job[DEPT_MANAGER],
                    duration = duration(job[START_DATE], job[END_DATE]))
                new_job.save()

        logger.info('Reading and print all Job rows')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def pprint_db():
    """
    Print summary of database to CLI
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Person class')
    logger.info('Printing summary of database content to CLI')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                     .select(Person, Job)
                     .join(Job, JOIN.LEFT_OUTER)
                    )

        print('**********************DATA SUMMARY*************************')
        print('\n')

        for person in query:
            try:
                print(f'Person {person.person_name} had job {person.job.job_name}')
                print(f'{person.person_name} reported to {person.job.department_manager} for {person.job.duration} days')
                print(f'in the {person.job.department_name} department')

            except Exception as e:
                print(f'Person {person.person_name} had no job')
        print('\n')
        print('********************END DATA SUMMARY***********************')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    database = SqliteDatabase('personjob.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only
    database.create_tables([
        Job,
        Person,
        PersonNumKey
    ])
    database.close()

    populate_persondata()
    populate_jobdata()
    pprint_db()
