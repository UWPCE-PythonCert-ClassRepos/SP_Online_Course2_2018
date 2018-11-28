"""
    Assignment 1: Query the database table
"""

from create_personjob import *
import logging



## INNER JOIN


    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                .select(Person, Job)
                .join(Job, JOIN.INNER)
                )

        logger.info('View matching records from both tables')
        for person in query:
            logger.info(f'Person {person.person_name} had job {person.job.job_name}')

    except Exception as e:
        logger.info(f'Error creating = {jon[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':


## LEFT_OUTER JOIN

    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    databse = SqliteDatabase('personjob.db')

    logger.info('View matching records and Persons without Jobs (note LEFT_OUTER)')

    try:
        databse.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Person
                 .select(Person, Job)
                 .join(Job,JOIN.LEFT_OUTER)
                 )

        for person in query:
            try:
                logger.info(f'Person {person.person_name} had job {person.job.jon_name}')

            except:
                logger.info(f'Person {person.person_name} had no job')

        logger.info('Example of how to summarize data')
        logger.info('Note select() creates a count and names it job_count')
        logger.info('group_by and order_by control level and sorting')

        query = (Person
                 .select(Person, fn.COUNT(Job.job_name).alias('job_count'))
                 .join(Job, JOIN.LEFT_OUTER)
                 .group_by(Person)
                 .order_by(Person.person_name)

        for person in query:
            logger.info(f'{person.person_name} had {person.job_count} jobs')

if __name__ == '__main__':
    
















