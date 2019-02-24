"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
import datetime

from personjob_model import *


def populate_people():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

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

    logger.info('populating person class')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in people:
            logger.info(f'building {person}')
            with database.transaction():
                new_person = Person.create(
                        person_name=person[PERSON_NAME],
                        lives_in_town=person[LIVES_IN_TOWN],
                        nickname=person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in '
                        f'{saved_person.lives_in_town} and likes to be known '
                        f'as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def populate_departments():
    """fills in the departments for database"""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('populating department class')

    NUMBER = 0
    NAME = 1
    MANAGER = 2

    departments = [
        ('D001', 'Marketing', 'Peter'),
        ('D002', 'Engineering', 'Pam'),
        ('D003', 'Sales', 'Peter'),
        ]

    logger.info('Creating Person records: iterate through the list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                        department_number=department[NUMBER],
                        department_name=department[NAME],
                        department_manager=department[MANAGER])
                new_department.save()
                logger.info('Database add successful')

        logger.info('Print the Department records we saved...')
        for saved_department in Department:
            logger.info(f'{saved_department.department_name} has manager '
                        f'{saved_department.department_manager}')

    except Exception as e:
        logger.info(f'Error creating = {department[NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def populate_jobs():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Job class')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Analyst', datetime.datetime(2001, 9, 22),
         datetime.datetime(2003, 1, 30), 65500, 'Andrew', 'D001'),
        ('Senior analyst', datetime.datetime(2001, 9, 22),
         datetime.datetime(2003, 1, 30), 70000, 'Andrew', 'D001'),
        ('Senior business analyst', datetime.datetime(2001, 9, 22),
         datetime.datetime(2003, 1, 30), 80000, 'Andrew', 'D002'),
        ('Admin supervisor', datetime.datetime(2001, 9, 22),
         datetime.datetime(2003, 1, 30), 45900, 'Peter', 'D002'),
        ('Admin manager', datetime.datetime(2001, 9, 22),
         datetime.datetime(2003, 1, 30), 45900, 'Peter', 'D002')
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
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED],
                    department=job[DEPARTMENT],)
                new_job.save()

        logger.info('Reading and print all Job rows')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} '
                        f'for {job.person_employed}')
            logger.info(f'days on job: {job.days_in_job}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def report_persons_departments():
    """creates report of all departments person worked"""
    query = (Person
             .select(Person.person_name,
                     Department.department_name,
                     Job.job_name)
             .join(Job, join_type=JOIN.LEFT_OUTER,
                   on=(Person.person_name == Job.person_employed))
             .join(Department, join_type=JOIN.LEFT_OUTER,
                   on=(Job.department == Department.department_number))
             .dicts()
             )

    for entry in query:
        print(entry)


if __name__ == '__main__':
    populate_people()
    populate_departments()
    populate_jobs()
    report_persons_departments()
