from pprint import pprint as pp
from create_database import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personnel_database.db')


def main():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job.select())
        pp('{:25} - {:10} - {:10} - {:5}'.format(
            'Job Name', 'Duration', 'Name', 'Department'))
        for job in query:
            pp('{:25} - {:10} - {:10} - {:5}'.format(
                job.job_name, job.duration, str(job.person_employed), str(job.job_department
            )))
    except Exception as e:
        logger.info(e)
    finally:
        database.close()

if __name__ == '__main__':
    main()
