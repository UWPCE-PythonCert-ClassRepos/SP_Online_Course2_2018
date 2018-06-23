from pprint import PrettyPrinter
from personjob_model import *

pp = PrettyPrinter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjob.db')

def pull_jobs():
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info("Pulling all the departments that a person has worked at.")
        query = (Job
                 .select(Job.job_dept, Job.job_name, Job.person_employed)
                 .order_by(Job.person_employed.desc(), Job.start_date.asc())
        )
        for job in query:
            print('\n'+'********')
            pp.pprint(job.job_dept)
            pp.pprint(job.job_name)
            pp.pprint(job.person_employed)
            print('********'+'\n')
    except Exception as e:
        logger.info(e)
    finally:
        database.close()


if __name__ == '__main__':
    pull_jobs()
