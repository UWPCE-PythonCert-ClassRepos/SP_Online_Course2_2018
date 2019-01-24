# ------------------------------------------------- #
# Title: Lesson 7, Database Management, Pretty Print Rev2
# Dev:   Craig Morton
# Date:  12/26/2018
# Change Log: CraigM, 1/12/2018, Database Management, Pretty Print Rev2
# ------------------------------------------------- #

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from create_db import *
from datetime import datetime, timedelta
import pprint
import logging


def populate_persons():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personnel_database.db')

    logger.info('Working with Person class')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Bill', 'Seattle', 'Billy'),
        ('Nikola', 'Croatia', 'Zappy'),
        ('Jeff', 'Seattle', 'Jeffy'),
        ('Elon', 'Los Angeles', 'Musky'),
        ('Linus', 'Helsinki', None),
        ('Steve', 'San Francisco', 'Stevie')
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

    finally:
        logger.info('database closes')
        database.close()


def populate_depts():
    """
        add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personnel_database.db')

    logger.info('Working with Department class')

    DPT_NUMBER = 0
    DPT_NAME = 1
    DPT_MANAGER = 2

    departments = [
        ('SYS', 'System Engineering', 'Sally Systems'),
        ('DEV', 'Software Engineering', 'Devin Developer'),
        ('NET', 'Network Engineering', 'Nina Networks')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dpt in departments:
            with database.transaction():
                new_department = Department.create(
                    dpt_number=dpt[DPT_NUMBER],
                    dpt_name=dpt[DPT_NAME],
                    dpt_manager=dpt[DPT_MANAGER])
                new_department.save()

        logger.info('Print the Department records we saved...')
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


def populate_jobs():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personnel_database.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DPT_NUMBER = 5

    jobs = [
        ('Systems Engineer', '2014-08-08', '2018-08-08', 80000, 'Nikola', 'SYS'),
        ('Systems Architect', '2012-09-09', '2016-09-09', 130000, 'Elon', 'SYS'),
        ('Software Developer', '2010-07-07', '2014-07-07', 90000, 'Linus', 'DEV'),
        ('Principal Developer', '2008-06-06', '2012-06-06', 1600000, 'Bill', 'DEV'),
        ('Network Engineer', '2000-04-04', '2008-04-04', 70000, 'Steve', 'NET'),
        ('Network Architect', '1996-03-03', '2006-03-03', 120000, 'Jeff', 'NET')
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

        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} ' + f'to {job.end_date} for {job.person_employed} ' +
                        f'dept_id: {job.departmnet}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def person_pretty_print():
    """
        Pretty print displaying all departments a person has worked
        as well as every job they've had, including duration.  Combines multiple tables.
    """
    database = SqliteDatabase('personnel_database.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    dbdata = Job.select(Job.person_employed).distinct()

    for names in dbdata:
        print("\nEmployee: {}".format(str(names.person_employed)))
        query = (Job.select(Person.person_name, Department.dpt_name, Department.dpt_number,
                            Job.start_date, Job.end_date).join(Person, on=(Person.person_name == Job.person_employed))
                 .join(Department, on=(Department.dpt_number == Job.departmnet))
                 .where(Person.person_name == names.person_employed).namedtuples())

        for row in query:
            days_worked = date_differential(row.end_date, row.start_date)
            out = ("Department Number: " + row.dpt_number,
                   "Department Name: " + row.dpt_name,
                   "Start Date: " + row.start_date,
                   "End Date: " + row.end_date,
                   "Duration of Employment: " + str(days_worked))
            pprint.pprint(out)


def date_differential(d1, d2):
    """
    Duration of employment.
    """
    date1 = datetime.strptime(d1, '%Y-%m-%d')
    date2 = datetime.strptime(d2, '%Y-%m-%d')
    return abs((date2 - date1).days)


if __name__ == '__main__':
    populate_persons()
    populate_depts()
    populate_jobs()
    person_pretty_print()
