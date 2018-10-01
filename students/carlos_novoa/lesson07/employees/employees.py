"""
This module contains refactored person and Job examples along
with new Department table and query
"""


from models import *  # noqa F403
import logging
import pprint
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('staff.db')  # noqa F403
pp = pprint.PrettyPrinter()


def add_people():

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
                new_person = Person.create(  # noqa F403
                        person_name=person[PERSON_NAME],
                        lives_in_town=person[LIVES_IN_TOWN],
                        nickname=person[NICKNAME])
                new_person.save()

        logger.info('People added.')

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def add_jobs():

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT_NUMBER = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'A100'),
        ('Senior analyst',
            '2003-02-01', '2006-10-22', 70000, 'Andrew', 'A100'),
        ('Senior business analyst',
            '2006-10-23', '2016-12-24', 80000, 'Andrew', 'A100'),
        ('Admin', '2012-10-01', '2014-11-10', 45900, 'Peter', 'B100'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'B100')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(  # noqa F403
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED],
                    in_department=job[DEPARTMENT_NUMBER])
                new_job.save()

        logger.info('Jobs added.')

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def add_departments():
    """
        This method adds departments data
        and confirms by pretty printing
    """

    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    departments = [
        ('A100', 'Finance', 'Finance Manager'),
        ('B100', 'Admin', 'Admin Manager')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info('Loop through sample data and create new row')
        logger.info('based on Department model that was imported above')

        for dept in departments:
            with database.transaction():
                new_dept = Department.create(  # noqa F403
                        department_number=dept[DEPARTMENT_NUMBER],
                        department_name=dept[DEPARTMENT_NAME],
                        department_manager=dept[DEPARTMENT_MANAGER])
                new_dept.save()

        logger.info('Departments added.')

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def query_departments():
    """
        This method queries departments to confirm data added correctly
    """
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        query = (Person.select(Person.person_name, Job)  # noqa F403
         .join(Job, JOIN.INNER))  # noqa F403

        employees = []
        for row in query:
            sd = datetime.strptime(row.job.start_date, "%Y-%m-%d")
            ed = datetime.strptime(row.job.end_date, "%Y-%m-%d")
            delta = ed - sd
            es = '{} {} {} {}'.format(row.person_name,
                                      row.job.job_name,
                                      row.job.in_department,
                                      delta.days)

            employees.append(es)
        pp.pprint(employees)

    except Exception as e:
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    # add_people()
    # add_departments()
    # add_jobs()
    query_departments()
