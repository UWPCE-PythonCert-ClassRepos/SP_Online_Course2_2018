from database_ex import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjob.db')


def printer():
    """
        Queries and prints information from the database.
    """
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info("Running Query")

        query = (Job.select())
        for job in query:
            print(f'{job.person_employed} was a {job.job_name} in the {job.job_department} for {job.job_duration} days. \n DEPT ID:{job.job_department.department_number}')

    except Exception as e:
        logger.error(e)
    finally:
        database.close()


if __name__ == "__main__":
    printer()