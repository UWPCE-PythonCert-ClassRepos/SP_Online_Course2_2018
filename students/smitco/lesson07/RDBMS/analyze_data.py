# Lesson 07 RDBMS exercise
# Base code from RDBMS example from website
# !/usr/bin/env python3

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from personjobdept_setup import *
from datetime import datetime

logger = logging.getLogger(__name__)
database = SqliteDatabase('personjobdept.db')
    
def analyze_days_on_job():
    """analyze days on job per person"""

    logger.info('Creating days on job analysis using Inner Join')
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                 .select(Person, Job)
                 .join(Job, JOIN.INNER)
                )

        for person in query:
            start = datetime.strptime(person.job.start_date, '%Y-%m-%d').date()
            end = datetime.strptime(person.job.end_date, '%Y-%m-%d').date()
            duration = (end - start).days
            print(f'{person.person_name} had job {person.job.job_name} for {duration} days')

    except Exception as e:
        logger.info(f'Error analyzing days on job for {person.person_name} as {person.job.job_name}')
        logger.info(e)
        logger.info(f'Analysis of data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()

def analyze_depts():
    """pretty print departments each person has worked in"""
    
    logger.info('Creating department employment analysis using Inner Join and pretty print')
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Department
                 .select(Department, Job)
                 .join(Job, JOIN.INNER)
                 )
        
        for dept in query:
            print(f'{dept.job.person_employed} worked in {dept.dept_name} as {dept.job.job_name}')
    
    except Exception as e:
        logger.info(f'Error analyzing departments for {dept.job.person_employed} as {dept.job.job_name}')
        logger.info(e)
        logger.info(f'Analysis of data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()

if __name__ == '__main__':
    analyze_days_on_job()
    analyze_depts()