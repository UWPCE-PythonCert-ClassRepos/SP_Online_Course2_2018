import logging
from personjob_model import *


def pretty_print():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    database = SqliteDatabase('personjob.db')

    logger.info('All of the departments a person worked in for every job they ever had')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info('Querying database.')

        query = Job.select(Job.person_employed, Job.job_name, Job.job_department).order_by(
                Job.person_employed.desc())

        for i in query:
            pers=[i.person_employed, i.job_name,i.job_department]
            print('\n')
            print('==================')
            print(pers)
            print('==================')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()


if __name__ == '__main__':
    pretty_print()
