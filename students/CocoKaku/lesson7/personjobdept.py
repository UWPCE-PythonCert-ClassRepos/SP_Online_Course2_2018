"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from personjobdept_model import *
from datetime import datetime

def populate_db_person():
    """
    populate database with persons
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

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

    logger.info('Creating Person records:')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    for person in people:
        try:
            with database.transaction():
                new_person = Person.create(
                        person_name = person[PERSON_NAME],
                        lives_in_town = person[LIVES_IN_TOWN],
                        nickname = person[NICKNAME])
                new_person.save()
            logger.info('   Database add successful')

        except Exception as e:
            logger.info(f'   Error creating = {person[PERSON_NAME]}: ' + str(e))

    logger.info('Print all Person records:')
    for saved_person in Person:
        logger.info(f'   {saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
            f'and likes to be known as {saved_person.nickname}')

    logger.info('database closes\n')
    database.close()

def populate_db_dept():
    """
    add departments to database
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    depts = [
        ('B202', 'Business Analysis', 'Mark'),
        ('A101', 'Administration', 'Roger'),
        ]

    logger.info('Create Department records:')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    for dept in depts:
        try:
            with database.transaction():
                new_dept = Department.create(
                        dept_number = dept[DEPT_NUMBER],
                        dept_name = dept[DEPT_NAME],
                        dept_manager = dept[DEPT_MANAGER])
                new_dept.save()
            logger.info('   Database add successful')

        except Exception as e:
            logger.info(f'   Error creating = {dept[DEPT_NUMBER]}, ' + str(e))

    logger.info('Print all Department records:')
    for saved_dept in Department:
        logger.info(f'   Department {saved_dept.dept_number} is {saved_dept.dept_name} ' +\
            f'and is managed by {saved_dept.dept_manager}')

    logger.info('database closes\n')
    database.close()


def populate_db_jobs():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT_NUMBER = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'B202'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'B202'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'A101'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'A101'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'A101'),
    ]

    logger.info('Create Job records:')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    for job in jobs:
        try:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    dept_number = job[DEPT_NUMBER])
                new_job.save()
            logger.info('   Database add successful')

        except Exception as e:
            logger.info(f'   Error creating = {job[JOB_NAME]}: ' + str(e))

    logger.info('Print all Job records:')
    for job in Job:
        logger.info(f'   {job.job_name} : {job.start_date} to {job.end_date} ' +\
                    f'for {job.person_employed} in Dept {job.dept_number}.')
                    #f'held for {(datetime.strptime(job.end_date, "%Y-%m-%d") - datetime.strptime(job.start_date, "%Y-%m-%d")).days} days.')

    logger.info('database closes\n')
    database.close()

def read_person_record():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjobdept.db')

    query = (Person
             .select(Person, Job, Department)
             .join(Job, JOIN.LEFT_OUTER)
             .join(Department, JOIN.LEFT_OUTER)
            )

    for person in query:
        try:
            logger.info(f'Person {person.person_name} had job {person.job.job_name} in {person.job.dept_number.dept_name} department')

        except Exception as e:
            logger.info(f'Person {person.person_name} had no job')
    logger.info('database closes\n')
    database.close()

if __name__ == '__main__':
    populate_db_person()
    populate_db_dept()
    populate_db_jobs()

    read_person_record()

