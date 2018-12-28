"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from pprint import pprint as pp
from datetime import datetime
from create_personjobdept import *

def calc_duration(start, end):
    """
        Small function that calculates the difference of time between two dates
        and exports that time in the form of 'days'.
    """
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    return abs((end - start).days)

def populate_db_person():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

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
        ('Steven', 'Colchester', None)
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
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def populate_db_job():
    """
    add job data to database
    """

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Job class')

    PERSON_EMPLOYED = 0
    JOB_NAME = 1
    START_DATE = 2
    END_DATE = 3
    SALARY = 4
    DEPARTMENT = 5

    jobs = [
        ('Andrew', 'Analyst', '2016-09-01', '2018-09-01', 60000, 'E109'),
#        ('Andrew', 'Sales Associate', '2012-01-01', '2016-09-01', 30000, 'S101'),
        ('Peter', 'Graphic_Designer', '2010-01-01', '2012-05-05', 45000, 'G202'),
        ('Susan', 'District_Manager', '2014-04-10', '2017-02-14', 85000, 'S101'),
        ('Pam', 'Salesperson', '2012-03-01', '2012-09-01', 75000, 'S101'),
        ('Steven', 'Help_Desk_Associate', '2017-01-01', '2017-02-01', 38000, 'E109')
        ]
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    person_employed=job[PERSON_EMPLOYED],
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    duration=calc_duration(job[START_DATE], job[END_DATE]),
                    salary=job[SALARY],
                    job_dept=job[DEPARTMENT])
                new_job.save()
                logger.info('Database add successful')

        logger.info('Print the Job records we saved...')
        for saved_job in Job:
            logger.info(f'{saved_job.person_employed} worked as a {saved_job.job_name} ' +\
                        f'from date {saved_job.start_date} until date {saved_job.end_date} ' +\
                        f'({saved_job.duration} days) with a salary of {saved_job.salary} ' +\
                        f'in department {saved_job.job_dept}')

    except Exception as e:
        logger.info(f'Error creating = {job[PERSON_EMPLOYED]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def populate_db_dept():
    """
    add job data to database
    """

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Department class')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
        ('E109', 'Human_Resources', 'Jackie_Love'),
        ('G202', 'Graphics_Department', 'Evan_Picasso'),
        ('S101', 'Sales', 'Janet_Everson')
        ]
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in departments:
            with database.transaction():
                new_department = Department.create(
                    department_number=dept[DEPT_NUMBER],
                    department_name=dept[DEPT_NAME],
                    department_manager=dept[DEPT_MANAGER])
                new_department.save()
                logger.info('Database add successful')

        logger.info('Print the Department records we saved...')
        for saved_dept in Department:
            logger.info(f'{saved_dept.department_manager} works in {saved_dept.department_name} ' +\
                f'identified by the code {saved_dept.department_number}.')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def pretty_print():
    """
    add job data to database
    """

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with the Pretty Printer')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job.select(Job, Department).join(Department))
        pp('-' * 58)
        pp('Job Name             Employee         Department          ')
        pp('-' * 58)
        for ind in query:
            pp(f'{ind.job_name:20} {str(ind.person_employed):16} {str(ind.job_dept.department_name):20}')
        pp('-' * 58)

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    populate_db_person()
    populate_db_dept()
    populate_db_job()
    pretty_print()
