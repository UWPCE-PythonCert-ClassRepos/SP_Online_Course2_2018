# -*- coding: utf-8 -*-

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from personjob_model import *
from datetime import datetime, timedelta
from dateutil.parser import parse
import pprint
import logging


def populate_pers():
    """add person"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Person class')
    logger.info('use constants and a list of tuples as a simple schema')
    logger.info('Normally you will have prompted for this from a user')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Brian', 'Everett', 'The Brain'),
        ('Bev', 'Edmonds', None),
        ('Kendra', 'Marysville', 'Boss'),
        ('Matt', 'Stanwood', 'Rockefeller'),
        ('Jared', 'Lake Stevens', None),
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
                        person_name=person[PERSON_NAME],
                        lives_in_town=person[LIVES_IN_TOWN],
                        nickname=person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in \
{saved_person.lives_in_town} ' + f'and likes to be known as \
{saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def populate_dept():
    """add department"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Dept class')

    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MGR = 2

    department = [
        ('A123', 'Office', 'Sue'),
        ('B123', 'Operations', 'Rick'),
        ('C123', 'Administration', 'Jim')]

    logger.info('Creating Department records: iterate through list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in department:
            with database.transaction():
                new_dept = Dept.create(
                        dept_num=dept[DEPT_NUM],
                        dept_name=dept[DEPT_NAME],
                        dept_mgr=dept[DEPT_MGR])
                new_dept.save()
                logger.info('Database add successful')

        logger.info('Print the Dept records we saved...')
        for saved_dept in Dept:
            logger.info(f'{saved_dept.dept_num} is part of the \
{saved_dept.dept_name} department ' + f'\
and is managed by {saved_dept.dept_mgr}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NUM]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def populate_jobs():
    """add job"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person.use the foreign key')

    JOB_NAME = 0
    DEPT = 1
    EMPLOYEE = 2
    PAY = 3
    START_DATE = 4
    END_DATE = 5

    jobs = [('Tech', 'A123', 'Brian', 65500, '05-27-1981', '05-27-2013'),
            ('Tech supervisor', 'A123', 'Brian', 70000,
            '05-27-2013', '05-27-2016'),
            ('Operations manager', 'B123', 'Brian',
            80000, '05-27-2016', '1-20-2018'),
            ('Admin supervisor', 'C123', 'Bev',
            45900, '10-05-1980', '11-10-2014'),
            ('Admin manager', 'C123', 'Bev',
            45900, '11-10-2014', '01-05-2018')]

    def conv(d1, d2):
        start = parse(d1)
        end = parse(d2)
        diff = end - start
        return diff.days

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():

                new_job = Job.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    job_len=conv(job[START_DATE], job[END_DATE]),
                    pay=job[PAY],
                    employee=job[EMPLOYEE],
                    dept=job[DEPT])

                new_job.save()

            logger.info('Reading and print all Job rows')

            logger.info(f'{new_job.job_name} : {new_job.start_date} to\
{new_job.end_date} for\
{new_job.employee} in {new_job.dept} for {new_job.job_len} days.')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def pers_jobs():
    """add pretty print"""

    database = SqliteDatabase('personjob.db')

    logger.info('Working pretty print job')

    try:

        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info("Getting jobs and depts worked")

        locate = (Job.select(Job.employee, Job.job_name,
                             Job.dept).order_by(Job.employee.desc()))

        for pers in locate:
            record = [pers.employee, pers.job_name, pers.dept]
            pp = pprint.PrettyPrinter(indent=10)
            pp.pprint(record)

    except Exception as e:
        logging.info(e)

    finally:
        database.close()

if __name__ == '__main__':

    populate_pers()
    populate_dept()
    populate_jobs()
    pers_jobs()
