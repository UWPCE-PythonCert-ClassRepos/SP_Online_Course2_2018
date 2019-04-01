import logging
from personjobdept_mod import *
from datetime import datetime



def populate_person():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('employee.db')

    logger.info('Working with Person class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for this from a user')

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
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

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


def populate_dept():
    """
    add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('employee.db')

    logger.info('Working with Department class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for this from a user')

    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MGR = 2

    depts = [
        ('C100', 'Consulting Services', 'Fobert Reldpausch'),
        ('E200', 'Environmental Consulting', 'Havid Derricks'),
        ('G300', 'Geographic Information Science', 'Ster Peenstrup')
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in depts:
            with database.transaction():
                new_dpt = Department.create(
                    dpt_number = dept[DEPT_NUM],
                    dpt_name = dept[DEPT_NAME],
                    dpt_manager = dept[DEPT_MGR],)
                new_dpt.save()

        logger.info('Reading and printing all departments rows...')
        for dept in Department:
            logger.info(f'{dept.dpt_number} : {dept.dpt_manager} manages {dept.dpt_name}')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_job():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('employee.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'C100'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'C100'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'C100'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'E200'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'E200')
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
                    duration = duration_calc(job[START_DATE], job[END_DATE]),
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_department = job[DEPARTMENT])
                new_job.save()
        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed} in {job.job_department}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def duration_calc(date1, date2):
    date1 = datetime.strptime(''.join(date1.split('-')), '%Y%m%d')
    date2 = datetime.strptime(''.join(date2.split('-')), '%Y%m%d')
    return (date2-date1).days


if __name__ == '__main__':
    populate_dept()
    populate_person()
    populate_job()