from datetime import datetime
from create_personjobdepartment import *

import pprint
import logging

def days_between(start_date, end_date):
    """
        take two DateField objects, return days between
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return abs((end_date - start_date).days)

def join_classes():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_department.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job
                 .select(Job, Department)
                 .join(Department, JOIN.INNER)
                )

        jobs = []

        for job in query:
            try:
                logger.info('send start_date and end_date to days_between()')
                logger.info(f'{job.person_employed.person_name} held position {job.job_name} '\
                            f'in department {job.department.department_name} '\
                            f'for {days_between(job.start_date, job.end_date)} days')

                job_info = {
                    'name': job.person_employed.person_name,
                    'title': job.job_name,
                    'department': job.department.department_name,
                    'days': days_between(job.start_date, job.end_date)
                }

                jobs.append(job_info)

            except Exception as e:
                logger.info(e)


    except Exception as e:
        logger.info(e)

    finally:
        print_jobs(jobs)
        database.close()

def print_jobs(jobs):
    """
        pretty print array of job dicts
    """
    if len(jobs) > 0:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(jobs)
    else:
        print('No jobs to print out')

if __name__ == '__main__':
    join_classes()
