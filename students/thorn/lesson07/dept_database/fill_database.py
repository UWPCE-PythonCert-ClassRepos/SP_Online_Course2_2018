"""
    Module to populate our sqlite database with people.
"""

import logging
import db_printer
from database_ex import *
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name=__name__)
database = SqliteDatabase('personjob.db')


def calc_days(day_1, day_2):
    """ Calculates the number of days between two dates using datetime. """
    date1, date2 = datetime.strptime(day_1, '%Y-%m-%d'), datetime.strptime(day_2, '%Y-%m-%d')
    return abs((date2 - date1).days)
    

def populate_people():
    """
    Populates the database with people info.
    """

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    info = [
        ("Theodore", "Charleston", "Ted"),
        ("Theo", "Memphis", None),
        ("Michael", "Athens", "Mike")
    ]

    logger.info("Populating people database")

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in info:
            with database.transaction():
                new_person = Person.create(
                    person_name = person[PERSON_NAME],
                    lives_in_town = person[LIVES_IN_TOWN],
                    nickname = person[NICKNAME]
                )
                new_person.save()
                logger.info("Database person saved.")
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')
    except Exception as e:
        logger.error(f"Unable to make database changes:\n{e}")
    finally:
        logger.info("Database closed.")
        database.close()


def populate_department():
    """
    Populates the database with department info.
    """
    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    info = [
        ("BANK", "Banking", "Toby"),
        ("ACCT", "Accounting", "Chris"),
        ("TCHR", "Teaching", "Teddy")
    ]

    logger.info("Populating department database.")

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in info:
            with database.transaction():
                new_dept = Department.create(
                    department_number = dept[DEPARTMENT_NUMBER],
                    department_name = dept[DEPARTMENT_NAME],
                    department_manager = dept[DEPARTMENT_MANAGER]
                )
                new_dept.save()
        
        logger.info("Printing department records saved.")
        for saved_department in Department:
            logger.info(f"{saved_department.department_name}'s number is {saved_department.department_number} and managed by {saved_department.department_manager}")
    except Exception as e:
        logger.error(f"Unable to make database changes:\n{e}")
    finally:
        logger.info("Database closed.")
        database.close()


def populate_jobs():
    """
    Populates the database with job info.
    """

    # Tuple positions
    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    # List of tuples containing static database info
    info = [
        ('Bank Teller', '2018-01-01', '2018-08-31', 30000, 'Theo', 'BANK'),
        ('Bean Counter', '2014-05-01', '2017-12-31', 80000, 'Theodore', 'ACCT'),
        ('Musician', '2013-05-01', '2016-12-31', 90000, 'Michael', 'TCHR')
    ]

    logger.info("Populating job database.")

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in info:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    job_duration = calc_days(job[END_DATE], job[START_DATE]),
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_department = job[DEPARTMENT]
                )
                new_job.save()
                logger.info("Job info saved.")
        
        logger.info("Printing job records saved.")
        logger.info('Print the Job records we saved...')
        for saved_job in Job:
            logger.info(f'{saved_job.person_employed} worked in the '
                        f'{saved_job.job_department} department as a '
                        f'{saved_job.job_name} for {saved_job.job_duration} '
                        f'days, from {saved_job.start_date} to '
                        f'{saved_job.end_date} with a salary of '
f'{saved_job.salary}.')
    
    except Exception as e:
        logger.error(f"Unable to make JOB changes : JOBS :\n{e}")
    finally:
        logger.info("Database closed.")
        database.close()



if __name__ == "__main__":
    populate_people()
    populate_department()
    populate_jobs()
    db_printer.printer()
