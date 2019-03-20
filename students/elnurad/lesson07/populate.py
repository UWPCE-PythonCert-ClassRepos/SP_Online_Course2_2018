from create_personjob import *
from datetime import datetime
import logging

def diff_dates(date1, date2):
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    return (date2 - date1).days

def populate_db():
    """
       add Person to a database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

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
        logger.info(f'Error creating = {person.person_name}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def populate_department():
    """
       add Department to a database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')


    logger.info('Working with Department class')
    logger.info('Creating Department records')

    DEPT_NUMBER = 0
    DEPT_NAME = 1
    MANAGER = 2

    departments = [
        ('T000', 'Logistics', 'Kevin'),
        ('L002', 'Analytics', 'Linda')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_dept = Department.create(
                    dept_number = department[DEPT_NUMBER],
                    dept_name = department[DEPT_NAME],
                    manager = department[MANAGER]
                    )
                new_dept.save()
                logger.info('database add succesful')

        logger.info('Reading and printing all departments')
        for dept in Department:
            logger.info(f"{dept.dept_number} is the  {dept.dept_name} department." 
                        f"Its manager's name is {dept.manager}.")

    except Exception as e:
        logger.info(f'Error creating = {dept.dept_name}')
        logger.info(e)

    finally:
        logger.info('database closed')
        database.close()


def populate_jobs():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')


    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    JOB_DEPT_ID = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'L002'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Peter', 'L002'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Peter', 'L002'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Pam', 'T000'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Susan', 'T000')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_department_numb = job[JOB_DEPT_ID],
                    job_duration = diff_dates(job[START_DATE], job[END_DATE]))
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')
            logger.info(f'{job.person_employed} worked in the {job.job_department_numb} for {job.job_duration} days.')

    except Exception as e:
        logger.info(f'Error creating = {job.job_name}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_db()
    populate_department()
    populate_jobs()
    
