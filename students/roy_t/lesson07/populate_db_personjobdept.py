#!/usr/bin/env python3

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from datetime import datetime, timedelta
from personjobdept_model import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
database = SqliteDatabase('personjobdept.db')


def populate_people():
    """
    add person data to database
    """

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
                logger.info(f'Added person successfully: {person[PERSON_NAME]}')

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
    Add jobs to the database
    """

    logger.info('Populating the db with jobs')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Reverse Software Engineer', '2011-02-28', '2012-04-24', 135000, 'Peter', 'IT'),
        ('Database Normalizer', '2000-03-12', '2009-12-12', 99000, 'Peter', 'IT'),
        ('Structural Engineer', '2015-12-09', '2019-02-02', 140000, 'Andrew1', 'SA'),
        ('Administrator', '2017-07-19', '2018-03-04', 75000, 'Andrew2', 'SA'),
        ('Staff Analyst', '2012-05-05', '2015-04-30', 89000, 'Andrew3', 'SA')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                job_dur = datetime.strptime(job[END_DATE], '%Y-%m-%d') - datetime.strptime(job[START_DATE], '%Y-%m-%d')
                logger.info(job_dur.days)
                new_job = Job.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    duration=str(job_dur.days),
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED],
                    job_department=job[DEPARTMENT]
                )

                new_job.save()
                logger.info('Job added to db successfully.')

        logger.info('Printing job rows...')
        for job in Job:
            logger.info(f'{job.person_employed} held the position of {job.job_name} from {job.start_date} to {job.end_date}')
    except Exception as e:
        logger.info(f'Error creating job: {job[JOB_NAME]}')
        logger.info(e)
    finally:
        logger.info('database closes')
        database.close()


def populate_departments():
    """
    Populate the db with department information.
    """

    logger.info('Populating departments...')

    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MGR = 2

    departments = [
        ('SA', 'Systems Architect', 'Frank Thetank'),
        ('ENG', 'Engineering', 'Susan Powerz'),
        ('HR', 'Human Resources', 'Dan Caretaker'),
        ('MA', 'Mobile Applications', 'Fred Flintstone')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in departments:
            with database.transaction():
                new_dept = Department.create(
                    dept_num=dept[DEPT_NUM],
                    dept_name=dept[DEPT_NAME],
                    dept_manager=dept[DEPT_MGR])
                new_dept.save()
                logger.info(f'Added department: {dept[DEPT_NAME]}')

        logger.info('Printing department rows...')
        for dept in Department:
            logger.info(f'{dept.dept_num}:{dept.dept_name}  Manager: {dept.dept_manager}')
    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_people()
    populate_departments()
    # populate_jobs()
