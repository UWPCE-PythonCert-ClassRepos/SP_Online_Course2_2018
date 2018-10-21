import logging
from personjob_model import *
from datetime import datetime
import pprint

def populate_db():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Person class')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
        ('Pam', 'Coventry', 'PJ'),
        ('Steven', 'Colchester', None),
        ]

    logger.info('Creating Person records: iterate through the list of tuples')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name = person[PERSON_NAME],
                        lives_in_town = person[LIVES_IN_TOWN],
                        nickname = person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()
        
    
    # Work with the Jobs class
    database = SqliteDatabase('personjob.db')

    logger.info('Working with Jobs class')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT_ID = 5

    jobs = [
        ('Data Scientist', '2012-01-01', '2014-01-01','100000.00','Andrew', 'A001'),
        ('Data Scientist II', '2014-01-01', '2018-01-01','150000.00','Andrew', 'A001'),
        ('Scientist', '2012-01-01', '2014-01-01','80000.00','Peter', 'A003'),
        ('Data Engineer', '2014-01-01', '2018-01-01','100000.00','Susan', 'A004'),
        ('Database Engineer', '2012-01-01', '2018-01-01','90000.50','Pam', 'A005'),
        ]

    logger.info('Creating jobs records: iterate through the list of tuples')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            end = datetime.strptime(job[END_DATE], "%Y-%m-%d")
            start = datetime.strptime(job[START_DATE], "%Y-%m-%d")
            dur = (end - start).days
            
            with database.transaction():             
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    dept_id = job[DEPT_ID],
                    duration = dur)
                new_job.save()
                logger.info('Database add successful')

        logger.info('Print the Job records we saved...')
        for saved_job in Job:
            logger.info(f'{saved_job.person_employed} makes ${saved_job.salary} ' +\
                f'at job {saved_job.job_name} for duration {saved_job.duration} days')

    except Exception as e:
        logger.info(f'Error creating = {jobs[PERSON_EMPLOYED]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


    # Work with the Departments class
    database = SqliteDatabase('personjob.db')

    logger.info('Working with Departments class')

    DEPT_ID = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [
        ('A001', 'Cosmetics', 'Billy'),
        ('A002', 'Grocery', 'Amanda'),
        ('A003', 'Computers', 'Shane'),
        ('A004', 'Electronics', 'Bob'),
        ('A005', 'Produce', 'Lilly'),
        ]

    logger.info('Creating department records: iterate through the list of tuples')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    dept_id = department[DEPT_ID],
                    dept_name = department[DEPT_NAME],
                    dept_manager = department[DEPT_MANAGER])
                new_job.save()
                logger.info('Database add successful')

        logger.info('Print the Department records we saved...')
        for saved_dept in Department:
            logger.info(f'{saved_dept.dept_id} is the ID for {saved_dept.dept_name} ' +\
                f'and the manager is {saved_dept.dept_manager}')

    except Exception as e:
        logger.info(f'Error creating = {departments[DEPT_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


def pretty_print_jobs():
    logger.info('Pretty Print Output:')
    
    database = SqliteDatabase('personjob.db')

    printer = pprint.PrettyPrinter()

    for job in Job:
        job_dept_print = (job.person_employed.person_name,
                          job.job_name,
                          job.dept_id.dept_name)
        printer.pprint(job_dept_print)

if __name__ == '__main__':
    populate_db()
    
    pretty_print_jobs()