#!/usr/bin/env python3

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from create_personjob import *
import pprint
from datetime import datetime


def populate_person_data():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.DEBUG)
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
        ('Steven', 'Colchester', None)
        ]

    logger.info('Creating Person records: iterate through the list of tuples')

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


def populate_department_data():
    """
        add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Department class')
    logger.info('Creating Department records')

    DPT_NUMBER = 0
    DPT_NAME = 1
    DPT_MANAGER = 2

    departments = [
        ('F001', 'Finance', 'Dominic Magee'),
        ('BU00', 'Business Operations', 'Tamara Burns'),
        ('BU05', 'Senior Business Analyst', 'Elvin Ryce'),
        ('AD01', 'Administration', 'Tiana Colby'),
        ('MG01', 'Management', 'Scott Huston')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dpt in departments:
            with database.transaction():
                new_dpt = Department.create(
                    dpt_number=dpt[DPT_NUMBER],
                    dpt_name=dpt[DPT_NAME],
                    dpt_manager=dpt[DPT_MANAGER])
                new_dpt.save()

        logger.info('Read and print all Department rows')
        for dpt in Department:
            logger.info(f'dpt number: {dpt.dpt_number} ' +
                        f'dpt name: {dpt.dpt_name} ' +
                        f'dpt manager: {dpt.dpt_manager}')

    except Exception as e:
        logger.info(f'Error creating = {dpt[DPT_NUMBER]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_job_data():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with the Job class')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DPT_NUMBER = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'F001'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'BU00'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'BU05'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'AD01'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'MG01')
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
                    departmnet=job[DPT_NUMBER])
                new_job.save()

        logger.info('Reading and printing all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} ' +
                        f'to {job.end_date} for {job.person_employed} ' +
                        f'dept_id: {job.departmnet}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def select_dpt_history():
    """
        Produces a list using pretty print that shows all of
        the departments a person worked in for every job they ever had.
    """
    database = SqliteDatabase('personjob.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    names = Job.select(Job.person_employed).distinct()

    for name in names:
        print("\nEmployee name: {}".format(str(name.person_employed)))
        query = (Job
                 .select(Person.person_name, Department.dpt_name, Department.dpt_number,
                         Job.start_date, Job.end_date)
                 .join(Person, on=(Person.person_name == Job.person_employed))
                 .join(Department, on=(Department.dpt_number == Job.departmnet))
                 .where(Person.person_name == name.person_employed)
                 .namedtuples())

        for row in query:
            days_worked = day_diff(row.end_date, row.start_date)
            out = ("Department number: " + row.dpt_number,
                   "Department name: " + row.dpt_name,
                   "Start Date: " + row.start_date,
                   "End Date: " + row.end_date,
                   "Days Worked: " + str(days_worked))
            pprint.pprint(out)


def day_diff(d1, d2):
    date1 = datetime.strptime(d1, '%Y-%m-%d')
    date2 = datetime.strptime(d2, '%Y-%m-%d')
    return abs((date2 - date1).days)


if __name__ == '__main__':
    populate_person_data()
    populate_department_data()
    populate_job_data()
    select_dpt_history()
