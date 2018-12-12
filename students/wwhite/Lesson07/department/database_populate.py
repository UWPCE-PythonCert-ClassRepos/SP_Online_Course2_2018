"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
    (but running this program does not require it)
"""
import logging
from database_model import *
from datetime import datetime
from pprint import pprint as pp


def date_difference(date_1, date_2):
    start_date = datetime.strptime(date_1, "%Y-%m-%d")
    end_date = datetime.strptime(date_2, "%Y-%m-%d")
    difference = end_date - start_date
    return difference.days


def populate_person():
    """
    add person data to database
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('employee.db')

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

    logger.info('Creating Person records: iterate through the list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to rollback on error')

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
            logger.info(f'{saved_person.person_name} lives in '
                        f'{saved_person.lives_in_town} '
                        f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def populate_dep():
    """
    add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('employee.db')

    logger.info('Working with Department class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for this from a user')

    DEP_NUMBER = 0
    DEP_NAME = 1
    DEP_MANAGER = 2

    deps = [
        ('ADMN', 'Administrative', 'Michael Scott'),
        ('SALS', 'Sales', 'Jim Halpert'),
        ('ACCT', 'Accounting', 'Oscar Martinez'),
        ('HMRS', 'Human Resources', 'Kelly Kapoor'),
        ('WRHS', 'Warehouse', 'Darryl Philbin')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dep in deps:
            with database.transaction():
                new_dep = Department.create(
                    dep_number=dep[DEP_NUMBER],
                    dep_name=dep[DEP_NAME],
                    dep_manager=dep[DEP_MANAGER])
                new_dep.save()
                logger.info('Database add successful')

        logger.info('Read and print all Department records we created...')
        for dep in Department:
            logger.info(f'{dep.dep_name} '
                        f'dep number is {dep.dep_number} '
                        f'and is managed by {dep.dep_manager} ')

    except Exception as e:
        logger.info(f'Error creating = {dep[DEP_NUMBER]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def populate_job():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('employee.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'ACCT'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'HMRS'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'SALS'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'ADMN'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'ADMN')
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
                    job_duration = date_difference(job[END_DATE], job[START_DATE]),
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_dep = job[DEPARTMENT])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def printer():
    database = SqliteDatabase('employee.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Query the database')
        query = (Job.select())

        pp('{:^25}|{:^25}|{:^25}'.format(
            'Job Title', 'Person Employed', 'Department'))
        for job in query:
            pp('{:30} {} {:>35}'.format(
                job.job_name, job.person_employed, str(job.job_dep)))

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    populate_person()
    populate_dep()
    populate_job()
    printer()
