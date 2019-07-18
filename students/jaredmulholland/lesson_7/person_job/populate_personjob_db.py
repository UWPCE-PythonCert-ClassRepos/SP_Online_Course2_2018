"""
Student: Jared Mulholland
Lesson_7 Assignment 1

We have details of Persons. We have details of Jobs. Now we need to track in which Department a Person held a Job. 
For a Department, we need to know it's department number, which is 4 characters long and start with a letter. 
We need to know the department name (30 characters), and the name of the department manager (30 characters). 
We also need to know the duration in days that the job was held. Think about this last one carefully.

Make the necessary changes, annotating the code with log statements to explain what's going on. 
Also, draw a diagram to help think through how you will incorporate Department into the programs.

Finally, produce a list using pretty print that shows all of the departments a person worked in for every job they ever had. 
"""

import logging
import pprint
from datetime import datetime as dt
from personjob_model import *

def populate_person_db():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')
    
    logger.info('Working with person class')
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


def populate_job_db():
    """ add job data to database"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Job Class')
    logger.info('Creating job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT_NUM = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'A001'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'A002'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'A003'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'O001'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'O002')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            start_dt = dt.strptime(job[START_DATE], '%Y-%m-%d')
            end_dt = dt.strptime(job[END_DATE], '%Y-%m-%d')
            days = (end_dt - start_dt).days

            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    days_in_job = days,
                    dept_num = job[DEPT_NUM])
                new_job.save()

        logger.info('Reading and print all jobs rows')
        for job in Job:
            logger.info(f'{job.job_name}: {job.start_date} to {job.end_date} for {job.person_employed} in dept {job.dept_num} for {job.days_in_job} days')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close() 

def populate_department_db():
    """ add department data to database"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with department Class')
    
    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
                    ('A001','Business Intel','Rod'),
                    ('A002','Data Science','Parker'),
                    ('A003','Tech Leadership','Kina'),
                    ('O001','Org Admin','Dave'),
                    ('O002','Org Leadership','Tony')
                    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    dept_num = department[DEPT_NUM],
                    dept_name = department[DEPT_NAME],
                    dept_manager = department[DEPT_MANAGER]
                )
            new_department.save()

        logger.info('reading and print all dept rows')
        for dept in Department:
            logger.info(f'{dept.dept_num} : {dept.dept_name} managed by {dept.dept_manager}')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPT_NUM]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

def pretty_print_db():
    """prints joined tables from personjob db"""

    logging.basicConfig(level = logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info("connecting to personjob.db")

    database.connect()

    pp = pprint.PrettyPrinter()

    logger.info("People, Job, Department List")
    for job in Job:
        job_qry = (job.person_employed.person_name,
                    job.job_name,
                    job.dept_num.dept_name)
        
        pp.pprint(f'Name: {job_qry[0]}, Job: {job_qry[1]}, Dept: {job_qry[2]}')      
    
    
        
if __name__ == '__main__':
    populate_person_db()
    populate_department_db()
    populate_job_db()
    pretty_print_db()

