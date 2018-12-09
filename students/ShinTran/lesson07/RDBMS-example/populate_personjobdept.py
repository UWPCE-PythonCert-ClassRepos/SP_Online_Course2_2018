"""
    This program populates the person, job, and department tables
"""


import logging
from datetime import datetime
from create_personjobdept import *


def calc_datediff(d1, d2):
    """
    Returns the number of days between two date values
    """
    d1 = datetime.strptime(d1, '%Y-%m-%d')
    d2 = datetime.strptime(d2, '%Y-%m-%d')
    return abs((d2 - d1).days)


def populate_person():
    """
    Adds person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Meyton Panning', 'Denver', 'Sheriff'),
        ('Bom Trady', 'Boston', 'TB'),
        ('Brew Drees', 'New Orleans', None),
        ('Raron Aodgers', 'Green Bay', 'AR'),
        ('Wussell Rilson', 'Seattle', None)
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


def populate_job():
    """
        Adding job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT_NAME = 5


    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Brew Drees', 'Data Analytics'),
        ('Senior Analyst', '2003-02-01', '2006-10-22', 70000, 'Wussell Rilson', 'Data Analytics'),
        ('Senior Business Analyst', '2006-10-23', '2016-12-24', 80000, 'Meyton Panning', 'Data Analytics'),
        ('Admin Supervisor', '2012-10-01', '2014-11-10', 45900, 'Raron Aodgers', 'Human Resources'),
        ('Admin Manager', '2014-11-14', '2018-01-05', 45900, 'Bom Trady', 'Human Resources')
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
                    duration = calc_datediff(job[END_DATE], job[START_DATE]),
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    department_name = job[DEPARTMENT_NAME])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for sv_job in Job:
            logger.info(f'{sv_job.job_name} : {sv_job.start_date} to {sv_job.end_date} for {sv_job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_department():
    """
    Adds department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    DEPTARTMENT_ID = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    depts = [
        ('HR00', 'Human Resources', 'Ratt Myan'),
        ('DATA', 'Data Analytics', 'Gared Joff')
    ]

    logger.info('Creating Department records: iterate through the list of tuples')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in depts:
            with database.transaction():
                new_dept = Department.create(
                        department_id = dept[DEPTARTMENT_ID],
                        department_name = dept[DEPARTMENT_NAME],
                        department_manager = dept[DEPARTMENT_MANAGER])
                new_dept.save()
                logger.info('Database add successful')

        logger.info('Print the Dept records we saved...')
        for dept_saved in Department:
            logger.info(f'{dept_saved.department_manager} is the manager for the {dept_saved.department_name} department')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPARTMENT_NAME]}')
        logger.info(e)
        logger.info('The database keeps the records clean')

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_person()
    populate_department()
    populate_job()
