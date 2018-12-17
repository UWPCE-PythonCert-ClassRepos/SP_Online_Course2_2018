'''
Sean Tasaki
11/22/2018
Lesson07
populate_personjobdept
'''

from personjobdept_model import *
import logging
import pprint


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

def pretty_print_query():
    """
    A list using pretty print that shows all of the departments 
    a person worked in for every job they ever had.
    """

    database = SqliteDatabase('personjob.db')
    logger.info('calling person_jobs method')

    try:

        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info("Getting jobs and depts worked")

        locate = (Job.select(Job.person_employed, Job.job_name,
                             Job.job_department).order_by(Job.person_employed.desc()))

        for job in locate:
            record = [job.person_employed, job.job_name, job.job_department]
            pp = pprint.PrettyPrinter(indent=10)
            pp.pprint(record) 

    except Exception as e:
        logging.info(e)

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
            ('HR Speciaist', '2003-01-30', '2005-01-30', 804, 50000, 'Sean', 'H100'),
            ('Accountant I', '2005-01-30', '2008-02-28', 390, 55000, 'Sean', 'A100'),
            ('Accountant Supervisor', '2008-02-28', '2018-12-13', 3600, 80000, 'Sean', 'A100'),
            ('Senior analyst', '2003-02-01', '2006-10-22', 1359, 70000, 'Tom', 'A100'),
            ('Operations Supervisor', '2006-10-22', '2008-10-22', 730, 1200000, 'Tom', 'R100'),
            ('Computer Operator','2018-07-09', '2018-11-30', 122, 40000, 'MonkeyMan', 'R100')
            ]

    departments = [('R100', 'Operations', 'BigBoss'),
                   ('A100', 'Accounting', 'Allen'),
                   ('M100', 'Marketing', 'Mindy'),
                   ('H100', 'HR', 'Lucy')]

    add_people(people)
    add_departments(departments)
    add_jobs(jobs)
    pretty_print_query()
