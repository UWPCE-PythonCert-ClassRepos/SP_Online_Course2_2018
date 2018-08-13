#!/usr/bin/env python

from database_structure import *
import logging
from datetime import datetime
import pprint

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def populate_db():
    """
        add job data to database
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
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

    logger.info('Working with Department class')

    DEPARTMENT_ID = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    departments = [
        ('MATH', 'Math', 'Albert Einstein'),
        ('PHYS', 'Physics', 'Stephen Hawking'),
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                        department_id=department[DEPARTMENT_ID],
                        department_name=department[DEPARTMENT_NAME],
                        department_manager=department[DEPARTMENT_MANAGER])
                new_department.save()
                logger.info('Database add successful')

        logger.info('Print the Department records we saved...')
        for saved_department in Department:
            logger.info(f'{saved_department.department_id} is the '
                        f'{saved_department.department_name} department, '
                        f'managed by {saved_department.department_manager}.')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_ID]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

    logger.info('Working with Job class')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'MATH'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'MATH'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'PHYS'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'PHYS'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'PHYS')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                        job_name=job[JOB_NAME],
                        start_date=job[START_DATE],
                        end_date=job[END_DATE],
                        time_in_job=days_between(job[END_DATE], job[START_DATE]),
                        salary=job[SALARY],
                        person_employed=job[PERSON_EMPLOYED],
                        department_id=job[DEPARTMENT])
                new_job.save()
                logger.info('Database add successful')

        logger.info('Print the Job records we saved...')
        for saved_job in Job:
            logger.info(f'{saved_job.person_employed} worked in the '
                        f'{saved_job.department_id} department as a '
                        f'{saved_job.job_name} for {saved_job.time_in_job} '
                        f'days, from {saved_job.start_date} to '
                        f'{saved_job.end_date} with a salary of '
                        f'{saved_job.salary}.')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def output():

    database = SqliteDatabase('personjob.db')

    printer = pprint.PrettyPrinter()

    for job in Job:
        job_dept = (job.person_employed.person_name,
                    job.job_name,
                    job.department_id.department_name)
        printer.pprint(job_dept)


if __name__ == '__main__':
    populate_db()
    output()