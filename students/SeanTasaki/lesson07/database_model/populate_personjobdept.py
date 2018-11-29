'''
Sean Tasaki
11/22/2018
Lesson07
'''

from personjobdept_model import *
import logging


def add_people(people):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2


    logger.info("Adding people to database")
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in people:
            with database.transaction():
                logger.info(f'{person[PERSON_NAME]}')
                cur_person = Person.create(person_name = person[PERSON_NAME], lives_in_town = person[LIVES_IN_TOWN], nickname = person[NICKNAME])                      
                cur_person.save()

                logger.info(f'Added {person[PERSON_NAME]} successfully to Person table.')

    except Exception as e:
        logger.info(f'Error creating entry for {person[PERSON_NAME]}')
        logger.info(e)

    finally:
        logger.info('close database')
        database.close()

def add_departments(departments):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MGR = 2

    logger.info("Add departments to database")
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in departments:
            with database.transaction():               
                cur_dept = Department.create(dept_num=dept[DEPT_NUM],
                                            dept_name=dept[DEPT_NAME],
                                            dept_manager=dept[DEPT_MGR])
                cur_dept.save()
                logger.info(f'Added {dept[DEPT_NAME]} successfully to Department table.')  
    
    except Exception as e:
        logger.info(f'Error creating entry for {dept[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('close database')
        database.close() 
    

def add_jobs(jobs):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    DURATION = 3
    SALARY = 4
    PERSON_EMPLOYED = 5
    JOB_DEPARTMENT = 6

    logger.info("Adding jobs to database")
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():               
                cur_job = Job.create(job_name=job[JOB_NAME],
                           start_date=job[START_DATE],
                           end_date=job[END_DATE],
                           duration_days=job[DURATION],
                           salary=job[SALARY],
                           person_employed=job[PERSON_EMPLOYED],
                           job_department=job[JOB_DEPARTMENT]
                           )
                cur_job.save()
                logger.info(f'Added {job[JOB_NAME]} successfully to Job table.')  

    except Exception as e:
        logger.info(f'Error creating entry for {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('close database')
        database.close() 
        

if __name__ == '__main__':

    people = [('Sean', 'Boston', 'Billy'),
              ('Filippo', 'Manchester', None),
              ('CoconutMan', 'New York', 'Clichy'),
              ('MonkeyMan', 'Asheville', 'MM'),
              ('Tom', 'Austin', 'Heartbreaker'),
              ]
    
    jobs = [('Engineer', '2001-09-22', '2003-01-30', 495, 65500, 'Sean', 'R100'),
            ('Senior analyst', '2003-02-01', '2006-10-22', 1359, 70000, 'Tom', 'A100'),
            ]

    departments = [('R100', 'Operations', 'BigBoss'),
                   ('A100', 'Accounting', 'Allen'),
                   ('M100', 'Marketing', 'Mindy'),
                   ('H100', 'HR', 'Lucy')]

    add_people(people)
    add_departments(departments)
    add_jobs(jobs)
