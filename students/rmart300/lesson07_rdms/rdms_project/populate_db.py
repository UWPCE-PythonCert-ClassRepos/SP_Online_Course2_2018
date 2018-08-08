"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from personjob_model import *

def populate_person_table():
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

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)

    finally:
        database.close()

def populate_department_table():
    """
        add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Department class')

    DEPARTMENT_NUM = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    departments = [
        ('0001', 'Finance', 'Andrew'),
        ('0002', 'Administrative', 'Susan'),
        ('0003', 'IT', 'Peter'),
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in departments:
            with database.transaction():
                new_dept = Department.create(
                    department_num = dept[DEPARTMENT_NUM],
                    department_name = dept[DEPARTMENT_NAME],
                    department_manager = dept[DEPARTMENT_MANAGER])
                new_dept.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPARTMENT_NAME]}')
        logger.info(e)

    finally:
        database.close()


def populate_job_table():
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
    JOB_DEPARTMENT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 1, 1),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 1, 1),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 1, 1),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 2, 3),
        ('Admin manager', '2014-11-14', '2018-01,05', 45900, 2, 3)
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
                    job_department = job[JOB_DEPARTMENT])
                new_job.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    populate_person_table()

    populate_department_table()

    populate_job_table()
