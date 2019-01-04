# Lesson 07 RDBMS exercise
# Base code from RDBMS example from website
# !/usr/bin/env python3

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from personjobdept_setup import *

logger = logging.getLogger(__name__)
database = SqliteDatabase('personjobdept.db')

def populate_people():
    """
    add person data to database
    """

    logger.info('Populating Person Data')

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

    logger.info('Trying to add Person data')

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
                logger.info('Person to Database add successful')

        logger.info('The Person records we saved:')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info(f'Population of data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()

def populate_dept():
    """
        add department data to database
    """

    logger.info('Populating Department Data')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2


    depts = [
        ('I100', 'Junior IT', 'George F.'),
        ('I200', 'Senior IT', 'George F.'),
        ('A100', 'Administration', 'Susan Q.'),
        ('M400', 'Managment', 'Jane D.')
        ]

    logger.info('Trying to add Department data')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in depts:
            with database.transaction():
                new_dept = Department.create(
                    dept_number = dept[DEPT_NUMBER],
                    dept_name = dept[DEPT_NAME],
                    dept_manager = dept[DEPT_MANAGER])
                new_dept.save()
                logger.info('Department to Database add successful')

        logger.info('The Department records we saved:')
        for dept in Department:
            logger.info(f'{dept.dept_number} : {dept.dept_name} managed by {dept.dept_manager}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NUMBER]}')
        logger.info(e)
        logger.info(f'Population of data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()

def populate_job():
    """
        add job data to database
    """

    logger.info('Populating Job Data')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    JOB_DEPT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'I100'),
        ('Senior Analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'I200'),
        ('Senior Business Analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'I200'),
        ('Admin Supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'A100'),
        ('Admin Manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'M400')
        ]

    logger.info('Trying to add Job data')
    
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
                    job_dept = job[JOB_DEPT])
                new_job.save()
                logger.info('Job to Database add successful')

        logger.info('The Job data we saved:')
        for job in Job:
            logger.info(f'{job.job_name} in Department {job.job_dept}: {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)
        logger.info(f'Population of data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()

if __name__ == '__main__':
    populate_people()
    populate_dept()
    populate_job()