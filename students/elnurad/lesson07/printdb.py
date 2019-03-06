from create_personjob import *
from populate import *
import logging
import pprint

def print_db():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        query = (Job
                .select(Job, Department)
                .join(Department, JOIN.INNER)
                 )
        
        logger.info('viewing and printing matching records from all tables')
        for job in query:
            pp = pprint.PrettyPrinter()
            job_dept = (job.person_employed.person_name,
                        job.job_name,
                        job.job_department_numb.dept_name)
            pp.pprint(job_dept)
               

    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    print_db()


