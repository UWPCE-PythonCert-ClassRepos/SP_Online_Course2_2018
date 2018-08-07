import logging
from personjob_model import *
from datetime import datetime


def date_diff(date1, date2):
    start_date = datetime.strptime(date1, "%Y-%m-%d")
    end_date = datetime.strptime(date2, "%Y-%m-%d")
    delta = end_date - start_date
    return delta.days


def populate_person():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Person class')
    logger.info('Note how I use constants and a list of tuples as a simple '
                'schema')
    logger.info('Normally you probably will have prompted for this from a '
                'user')

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


def populate_dept():
    """
    add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Deparment class')
    logger.info('Note how I use constants and a list of tuples as a simple '
                'schema')
    logger.info('Normally you probably will have prompted for this from a '
                'user')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    depts = [
        ('AD01', 'Admin', 'Manager1'),
        ('HR02', 'Human Resources', 'Manager2'),
        ('AN03', 'Analyst', 'Manager3'),
        ('SO04', 'Software', 'Manager4'),
        ('TE05', 'Tech', 'Manager5'),
        ]

    logger.info('Creating Department records: iterate through the list of '
                'tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in depts:
            with database.transaction():
                new_dept = Department.create(
                        dept_number=dept[DEPT_NUMBER],
                        dept_name=dept[DEPT_NAME],
                        dept_manager=dept[DEPT_MANAGER])
                new_dept.save()
                logger.info('Database add successful')

        logger.info('Print the Department records we saved...')
        for saved_dept in Department:
            logger.info(f'{saved_dept.dept_name} has '
                        f'dept number {saved_dept.dept_number} '
                        f'with {saved_dept.dept_manager} as manager')

    except Exception as e:
        logger.info(f'Error creating = {depts[DEPT_NUMBER]}')
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

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'AN03'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'AN03'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'AN03'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'HR02'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'AD01')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name= job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED],
                    job_dept=job[DEPT],
                    duration=date_diff(job[START_DATE], job[END_DATE])
                    )
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_dept} - {job.job_name} : '
                        f'{job.start_date} to {job.end_date}, '
                        f'({job.duration} days),'
                        f'for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def print_jobs():
    database = SqliteDatabase('personjob.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job.select())
        for job in query:
            to_print = [job.person_employed, job.job_name, job.job_dept]
            print(to_print)

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    populate_person()
    populate_dept()
    populate_job()
    print_jobs()
