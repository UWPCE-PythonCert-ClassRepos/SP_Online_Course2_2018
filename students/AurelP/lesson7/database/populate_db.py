"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from create_database import *
from datetime import datetime, timedelta
from pprint import pprint as pprint
import logging

#database = SqliteDatabase('person_job_dept.db')

def date_type(date):
   return datetime.strptime(''.join(date.split('-')), '%Y%m%d')

def dates_diff(date2, date1):
    return (date_type(date2)-date_type(date1)).days

def populate_persons():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_dept.db')

    logger.info('Working with Person class')

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

    finally:
        logger.info('database closes')
        database.close()

def populate_depts():
    """
    add departments data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_dept.db')

    logger.info('Working with Department class')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    depts = [
        ('HR00', 'Human Resources', 'John Doe'),
        ('BUS0', 'Business', 'Joanna Doe')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in depts:
            with database.transaction():
                new_dept = Department.create(
                    dept_number = dept[DEPT_NUMBER],
                    dept_name = dept[DEPT_NAME],
                    dept_manager = dept[DEPT_MANAGER],)
                new_dept.save()

        logger.info('Print the Department records we saved...')
        for dept in Department:
            logger.info(f'{dept.dept_number} : {dept.dept_manager} ' +\
                        f'manages {dept.dept_name}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_jobs():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_dept.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'BUS0'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'BUS0'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'BUS0'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'HR00'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'HR00')
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
                    duration_days = dates_diff(job[END_DATE], job[START_DATE]),
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_department = job[DEPARTMENT])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.duration_days} days from {job.start_date} to {job.end_date} for {job.person_employed} in {job.job_department}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

def pp_print():
    database = SqliteDatabase('person_job_dept.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job.select())
        print ("--------------------------------------------------------------------------------------")
        pprint('{:25} - {:10} - {:15} - {:5}'.format(
            'Job Name', 'Duration', 'Name', 'Department'))
        print ("--------------------------------------------------------------------------------------")
        for job in query:
            pprint('{:25} - {:10} - {:15} - {:5}'.format(
                job.job_name, str(job.duration_days), str(job.person_employed.person_name), str(job.job_department.dept_name)
            ))
    except Exception as e:
        logger.info(f'Error printing')
        logger.info(e)
    finally:
        database.close()

if __name__ == '__main__':
    populate_persons()
    populate_depts()
    populate_jobs()

    pp_print()
