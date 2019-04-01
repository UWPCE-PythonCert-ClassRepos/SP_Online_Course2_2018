from pprint import pprint as ppt
from personjobdept_mod import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('employee.db')


def main():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info("Querying the database")
        query = (Job.select())
        ppt('{:25} | {:10} | {:10} | {:20}'.format(
            'Job Name', 'Duration', 'Name', 'Department'))
        ppt('-'*(75))
        for job in query:
            ppt('{:25} | {:10} | {:10} | {:20}'.format(
                job.job_name, job.duration, str(job.person_employed), job.job_department.dpt_name))
    except Exception as e:
        logger.info(e)
    finally:
        database.close()


if __name__ == '__main__':
    main()