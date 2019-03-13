"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from init_db import *

def populate_db():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

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

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5
    DURATION = 6

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'D456', 500),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'D456', 1100),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'B234', 2500),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter', 'C345', 620),
        ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter', 'A123', 838)
        ]

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
        ('A123', 'Human Resources', 'John P. Person'),
        ('B234', 'Janitorial', 'Robert V. Clean'),
        ('C345', 'Administration', 'Goober Pea'),
        ('D456', 'Engineering', 'Albert Einstein')
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

    try:
        logger.info('Populate the departments...')
        for dept in departments:
            with database.transaction():
                new_dept = Department.create(
                        dept_number = dept[DEPT_NUMBER],
                        dept_name = dept[DEPT_NAME],
                        dept_manager = dept[DEPT_MANAGER])
                new_dept.save()
                logger.info('Database add successful')

        logger.info('Print the department records we saved...')
        for saved_dept in Department:
            logger.info(f'{saved_dept.dept_number} is {saved_dept.dept_name} ' +\
                f'and is managed by {saved_dept.dept_manager}')

    except Exception as e:
        logger.info(f'Error creating = {departments[DEPT_NUMBER]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    try:
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    dept_employed = job[DEPARTMENT],
                    duration = job[DURATION])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    populate_db()