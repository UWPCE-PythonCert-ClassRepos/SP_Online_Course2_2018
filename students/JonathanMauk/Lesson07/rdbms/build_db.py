"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from create_personjobdept import *
from datetime import datetime


def populate_people():
    """
        Add Person data to database.
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

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
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +
                        f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def populate_jobs():
    """
        Add Jobs data to database.
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

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew'),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter'),
        ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter')
    ]

    # Little function to calculate duration in days between hire and end dates.
    def duration(first_date, second_date):
        first_date = datetime.strptime(first_date, '%Y-%m-%d')
        second_date = datetime.strptime(second_date, '%Y-%m-%d')
        return abs((second_date - first_date).days)

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name}: {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_departments():
    """
        Add Department data to database.
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    logger.info('Working with Department class.')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
        ('A105', 'Accounting', 'Amanda Gillis'),
        ('B205', 'Business Analytics', 'Portia Rossellini'),
        ('H305', 'Human Resources', 'James O\'Hare'),
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    dept_number=department[DEPT_NUMBER],
                    dept_name=department[DEPT_NAME],
                    dept_manager=department[DEPT_MANAGER])
                new_department.save()

        logger.info('Reading and print all Department rows...')
        for dept in Department:
            logger.info(f'{dept.dept_number}: {dept.dept_name} is managed by {dept.dept_manager}.')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_people()
    populate_jobs()
    populate_departments()
