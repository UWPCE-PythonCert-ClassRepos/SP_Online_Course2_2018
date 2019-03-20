from create_personjob_dept import *
from datetime import datetime

import logging
import pprint

def read_db():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    database = SqliteDatabase('personjobdept.db')

    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    
    query = (Department
             .select(Job, Department)
             .join(Job, JOIN.INNER)
            )
    try:
        for dept in query:
            duration = (datetime.strptime(dept.job.end_date, '%Y-%m-%d') - datetime.strptime(dept.job.start_date, '%Y-%m-%d')).days
            logger.info(f'The time which {dept.job.person_employed} worked as {dept.job.job_name} has been calculated.')
            logger.info(f'The employee {dept.job.person_employed} has worked under {dept.dept_name} for a period of {duration} days.')
    except Exception as e:
        logger.info(f'{dept.dept_name} has no jobs.')
        logger.info(e)
    
    database.close()    
    
if __name__ == '__main__':
    read_db()