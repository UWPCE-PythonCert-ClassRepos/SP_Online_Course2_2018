import logging
from personjob_model import *
import pprint

def populate_person_db():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
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
    JOB_DEPT = 5
    JOB_LENGTH = 6

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', '43R0', 2131),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'T1R3', 500),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', '43R0', 8),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter', '90WR', 258),
        ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter', '90WR', 3)
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
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_dept = job[JOB_DEPT],
                    job_length = job[JOB_LENGTH])
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

def populate_dept_db():
    """
        add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Department class')
    logger.info('Creating Department records: just like Person. We use the foreign key')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
        ('43R0', 'Aero', 'Adrian Newey'),
        ('T1R3', 'Tires', 'Michelin Man'),
        ('90WR', 'Engines', 'Robert Yates')
        ]
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    department_number = department[DEPT_NUMBER],
                    department_name = department[DEPT_NAME],
                    department_manager = department[DEPT_MANAGER])
                new_department.save()
    
        logger.info('Reading and print all Job rows (note the value of person)...')
        for department in Department:
            logger.info(f'{department.department_number} : {department.department_name} Manager is {department.department_manager}')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

def print_jobs():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Preparing printing of list of people.')

    database = SqliteDatabase('personjob.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    query = Job.select(Job.person_employed, Job.job_name, Job.job_dept)

    for job in query:
        job_list = [job.person_employed.person_name, job.job_name, job.job_dept.department_name]
        pp = pprint.PrettyPrinter()
        pp.pprint(job_list)

if __name__ == '__main__':
    populate_person_db()
    populate_job_db()
    populate_dept_db()
    print_jobs()