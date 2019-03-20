"""
Populates personjob Database
"""

from peewee import fn, SqliteDatabase
from personjob_model import Person, Job, Department

import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
database = SqliteDatabase('personjob.db')


def create_db():
    database.create_tables([
            Job,
            Person,
            Department
        ])


def populate_person():
    """
    Populate the person Table
    """

    logger.info('Populating Person table')
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

    logger.info('Iterating through tuples')

    try:
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


def populate_job():
    """
        add job data to database
    """
    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'mktg'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'mktg'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'mktg'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'comm'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'comm')
        ]

    try:
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED],
                    department=job[DEPARTMENT])
                new_job.save()
                logger.info('Database add successful')

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)


def populate_dept():
    """
    Populates department table
    """
    DEPT_ID = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
               ('mktg', 'Marketing', 'John'),
               ('acct', 'Accounting', 'Susan'),
               ('comm', 'Communications', 'Beowulf'),
               ('tech', 'Technology', 'Gilgamesh')
               ]

    try:
        for dept in departments:
            with database.transaction():
                new_dept = Department.create(
                    dept_id=dept[DEPT_ID],
                    dept_name=dept[DEPT_NAME],
                    dept_manager=dept[DEPT_MANAGER])
                new_dept.save()
                logger.info('Database add successful')

        logger.info('Reading and print all Department rows')
        for dept in Department:
            logger.info(f'{dept.dept_manager} leads the {dept.dept_name} department aka {dept.dept_id}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_ID]}')
        logger.info(e)


def pretty_print():
    query = (Person
             .select(Person,
                     Job,
                     Department,
                     (fn.JULIANDAY(Job.end_date) - fn.JULIANDAY(Job.start_date))
                     .cast('int').alias('job_length')
                     )
             .join(Job)
             .join(Department)
             .group_by(Job)
             .order_by(Person.person_name)
             )

    spacing = "{:<15} | {:<25} | {:<15} | {:>5}\n"

    heading = spacing.format('Person', 'Position', 'Department', 'Days at Job')
    print(heading)
    for p in query:
        text = spacing.format(p.person_name,
                              p.job.job_name,
                              p.job.department.dept_name,
                              p.job_length)
        print(text)


if __name__ == '__main__':
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        create_db()
        populate_person()
        populate_dept()
        populate_job()
        pretty_print()
    except Exception as e:
        logger.info(e)
    finally:
        logger.info('database closes')
        database.close()
