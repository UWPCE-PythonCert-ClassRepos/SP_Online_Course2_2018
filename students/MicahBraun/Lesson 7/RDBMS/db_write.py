# ---------------------------------------------------------------------------------------------
# AUTHOR:   Original structures from RDBMS_example personjob_learning_v3_p1.py
# STUDENT:  Micah Braun
# PROJECT NAME: db_write.py
# DATE CREATED: N/A
# UPDATED:  11/15/2018
# PURPOSE:  Module 07, pt 1
# DESCRIPTION:  Provides the functions to interact with/populate the relational database.
# ---------------------------------------------------------------------------------------------
from person_job_dept_setup import *
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def date_deltas(date1, date2):
    date1 = datetime.strptime(''.join(date1.split('-')), '%Y%m%d')
    date2 = datetime.strptime(''.join(date2.split('-')), '%Y%m%d')
    return (date2 - date1).days


def add_people():
    """
        Populates person table in database
    """

    logger.info('Working with Person class')

    FIRST_NAME = 0
    LAST_NAME = 1
    LIVES_IN_TOWN = 2
    NICKNAME = 3

    people = [
        ('Harry', 'Potter', 'Surrey', None),
        ('Albus', 'Dumbledore', 'Godrics Hollow', 'Dumbledore'),
        ('Tom', 'Riddle', 'London', 'Voldemort'),
        ('Sybill', 'Trelawney', 'London', None),
        ('Dudley', 'Dursley', 'Surrey', None)
    ]

    logger.info('Creating People records')
    try:
        for person in people:
            with database.transaction():
                new_person = Person.create(
                    first_name=person[FIRST_NAME],
                    last_name=person[LAST_NAME],
                    lives_in_town=person[LIVES_IN_TOWN],
                    nickname=person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.first_name} {saved_person.last_name} lives in {saved_person.lives_in_town} ' +
                        f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[FIRST_NAME]}  {person[LAST_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def add_departments():
    """
        Populates department table in database
    """
    logger.info('Working with Department class')
    logger.info('Creating Department records')

    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MGR = 2

    departments = [
        ('DA', 'Dark Arts', 'Voldemort'),
        ('STU', 'Student', 'Minerva McGonnigal'),
        ('ADM', 'Administration', 'Ministry of Magic'),
        ('EDU', 'Education', 'Albus Dumbledore')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in departments:
            with database.transaction():
                new_dept = Department.create(
                    department_number=dept[DEPT_NUM],
                    department_name=dept[DEPT_NAME],
                    department_manager=dept[DEPT_MGR])
                new_dept.save()
                logger.info('Database add successful')

        logger.info(
            'Reading and print all Department rows ...')
        for dept in Department:
            logger.info(f'{dept.department_number} : {dept.department_name} manager : {dept.department_manager}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def add_jobs():
    """
        Populates jobs table in database
    """
    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Y1 Hogwarts Student', '1990-09-01', '1991-05-05', 0, 'Harry', 'STU'),
        ('Y2 Hogwarts Student', '1991-09-02', '1992-05-06', 0, 'Harry', 'STU'),
        ('Hogwarts Headmaster', '1970-09-01', '1997-06-30', 100000, 'Albus', 'ADM'),
        ('Evil Villain', '1938-09-04', '1998-05-02', 500000, 'Tom', 'DA'),
        ('Teacher', '1980-09-12', '1997-05-16', 75000, 'Sybill', 'EDU')
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
                    duration=date_deltas(job[START_DATE], job[END_DATE]),
                    salary=job[SALARY],
                    emplid=job[PERSON_EMPLOYED],
                    job_department=job[DEPARTMENT])
                new_job.save()
                logger.info('Database add successful')

        logger.info(
            'Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.emplid}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    add_people()
    add_departments()
    add_jobs()
