"""
    Delete the database file to start over
    This module populates the database with person, job, and department information
"""

from create_personjob_dept import *

import logging

def populate_db():
    """
    Add person, job, department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
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
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name = person[PERSON_NAME],
                        lives_in_town = person[LIVES_IN_TOWN],
                        nickname = person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
    
    logger.info('Creating department records: just like Person. We use the foreign key')
    
    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
        ('A100', 'HR', 'Kristen'),
        ('B100', 'Engineering', 'Zack'),
        ('C000', 'PR', 'Jack')
#        ('9999','QC', 'Andy')
        ]

    try:
        for dept in departments:
            with database.transaction():
                new_dept = Department.create(
                    dept_num = dept[DEPT_NUM],
                    dept_name = dept[DEPT_NAME],
                    dept_manager = dept[DEPT_MANAGER])
                new_dept.save()

        for dept in Department:
            logger.info(f'Dept ID {dept.dept_num} : {dept.dept_name} with reporting manager {dept.dept_manager}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)
        
    logger.info('Creating Job records: just like Person. We use the foreign key')
    
    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT_EMPLOYED = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'HR'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'HR'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'Engineering'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'PR'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'HR')
        ]

    try:
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    dept_employed = job[DEPT_EMPLOYED])
                new_job.save()

        for saved_job in Job:
            logger.info(f'{saved_job.job_name} : {saved_job.start_date} to {saved_job.end_date} for {saved_job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)
    
    logger.info('database closes')
    database.close()

if __name__ == '__main__':
    populate_db()