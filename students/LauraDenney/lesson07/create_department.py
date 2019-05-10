''''This class defines Department, which maintains department info
    of Job by Person'''

import pprint
import logging
from personjobdepartment_model import *
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_department():
    '''add department data to database'''
    database = SqliteDatabase('personjob.db')

    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    departments = [
        ('A123', 'Accounting', 'Bob'),
        ('B456','Accounting', 'Joe'),
        ('C123','HR','Shelly'),
        ('D456','IT','Veronica'),
        ('E123','Payroll','Laura')]
    database.connect()
    logger.info('Connecting to Database')
    database.execute_sql('PRAGMA foreign_keys = ON;')
    try:
        index = 0
        logger.info('attempting adding data to Department table.')
        for job in Job.select():
            if "," in job.end_date:
                job.end_date = '-'.join(job.end_date.split(","))
                logger.info('Fixing error in date format')
                job.save()
            job.job_department = departments[index][DEPARTMENT_NUMBER]
            job.save()
            end = datetime.strptime(job.end_date,"%Y-%m-%d")
            start = datetime.strptime(job.start_date, "%Y-%m-%d")
            with database.transaction():
                new_department = Department.create(
                    department_number = departments[index][DEPARTMENT_NUMBER],
                    department_name = departments[index][DEPARTMENT_NAME],
                    department_manager = departments[index][DEPARTMENT_MANAGER],
                    job_duration = (end - start).days,
                    job_held = job.job_name)
                new_department.save()
            index += 1
    except Exception as e:
        logger.info('error encountered at previous step')
        logger.info(e)
    else:
        logger.info('data successfully added')
    finally:
        logger.info('database closes')
        database.close()

def run_query():
    '''runs a select statement showing department joined to person and job'''
    database = SqliteDatabase('personjob.db')
    try:
        logger.info('connecting to database')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                 .select(Person, Job)
                 .join(Job)
                 )
        logger.info('Showing all departments/jobs/people (inner join)')
        for person in query:
            fstring = (f'Person {person.person_name} had job '
                        f'{person.job.job_name} in department '
                        f'{person.job.job_department}.')
            logger.info(fstring)
    except Exception as e:
        logger.info(e)
    finally:
        logger.info("closing database")
        database.close()

if __name__ == '__main__':
    populate_department()
    run_query()
