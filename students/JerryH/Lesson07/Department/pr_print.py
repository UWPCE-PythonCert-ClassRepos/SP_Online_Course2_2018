from pprint import pprint as ppt
from database_model import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('employee.db')


def main():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info("Querying the database")
        query = (Job
                 .select()
                )
        ppt('{:25} | {:10} | {:10} | {:10}'.format(
            'Job Name', 'Duration', 'Name', 'Department'
        ))
        ppt('='*80)
        for job in query:
            ppt('{:25} | {:10} | {} | {}'.format(
                job.job_name, job.duration, job.person_employed, job.job_dept
            ))
    except Exception as e:
        logger.info(e)
    finally:
        database.close()


if __name__ == '__main__':
    main()
