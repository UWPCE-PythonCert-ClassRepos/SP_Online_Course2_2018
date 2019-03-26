#!/usr/bin/env python3

"""
Lesson07 final requirement. Print the people, their job, and the department info.
"""

import pprint
from personjobdept_model import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjobdept.db')


def print_personjobdept():
    """
    Print the job information that each person has held, including department info.
    """

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for job in Job:
            pprint.pprint(f'{job.person_employed} was employed as a {job.job_name} from {job.start_date} to {job.end_date}. A total of {job.duration} days.')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    print_personjobdept()
