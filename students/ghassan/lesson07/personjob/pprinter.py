from pprint import pprint as pp
from db_model import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personnel.db')


def main():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info("Querying the database")
        query = (Job
                 .select()
                )
        pp('{:25} - {:10} - {} - {}'.format(
            'Job Name', 'Duration', 'Name', 'Department'
        ))
        for job in query:
            pp('{:25} - {:10} - {} - {}'.format(
                job.job_name, job.duration, job.person_employed, job.job_dept
            ))
            # pp(job.job_name)
            # pp(job.start_date)
            # pp(job.end_date)
    except Exception as e:
        logger.info(e)
    finally:
        database.close()


if __name__ == '__main__':
    main()
