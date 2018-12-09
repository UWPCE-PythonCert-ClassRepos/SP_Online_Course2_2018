# ---------------------------------------------------------------------------------------------
# AUTHOR:   Micah Braun
# PROJECT NAME: database_pp.py
# DATE CREATED: 11/16/2018
# UPDATED:  11/17/2018
# PURPOSE:  Module 07, pt 1
# DESCRIPTION:  Function queries the database for values to print out, and
#               prints out error messages accordingly if the try: block
#               fails.
# ---------------------------------------------------------------------------------------------
from pprint import pprint as pp
from person_job_dept_setup import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('print_personnel.db')


def pp_records():
    """
        Queries the database and prints out data using pprint
        to format output in an easier-to-read format
    """
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info('Querying database.')
        query = (Job
                 .select())
        pp('{:<20}   {}     {:<10}   {:<5}'.format(
            'Job Name', 'Duration', 'Name', 'Department'
        ))
        for job in query:
            pp('{:<20}   {:<8}     {:<10}   {:<5}'.format(
                job.job_name, job.duration, str(job.emplid), str(job.job_department)))

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    pp_records()
