import logging
from datetime import date
from personjob_model import *


database = SqliteDatabase('personjob.db')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_people():
    #Model: Name, Town, Nickname
    
    logging.info('Populating the DB with People')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [('Andrew', 'Seattle', 'Drew'),
              ('Matthew', 'Seattle', 'Matt'),
              ('Elizabeth', 'Tacoma', 'Lizzo'),
              ('Shang', 'Wallingford', None),
              ('Scott', 'Austin', None),
              ('Sharon', 'Los Angeles', None),
              ('Mei', 'Spokane', None),
              ('Brandon', 'Houston', 'Brando'),
              ('Emelia', 'La Grange', 'Emmy'),
              ('Benjamin', 'Reno', 'Ben'),
              ('Peter', 'Stuttgart', 'Pete')]
    
    logging.info('Creating person records by iterating through tuples')

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

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} and likes to be known as {saved_person.nickname}')
        logger.info('database closes')
        database.close()


def populate_departments():

    logging.info('Working with Department class')
    logging.info('Creating Department records.')

    DEPT_NUM = 0
    DEPT_NAME = 1
    DEPT_MANAGER = 2

    departments = [('ACNT', 'Accounting', 'Sharon'),
                   ('PR01', 'Public Relations', 'Elizabeth'),
                   ('ENGR', 'Engineering', 'Emelia'),
                   ('ADMN', 'Administration', 'Peter'),
                   ('SFTW', 'Software Development', 'Brandon'),
                   ('ANAL', 'Analysis', 'Andrew'),
                   ('8=))', 'Bad Dept num', 'Matthew')]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for dept in departments:
            with database.transaction():
                new_dept = Department.create(
                    dept_num = dept[DEPT_NUM],
                    dept_name = dept[DEPT_NAME],
                    dept_manager = dept[DEPT_MANAGER])
                new_dept.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('Print the Department records we saved...')
        for saved_dept in Department:
            logger.info(f'NUM={saved_dept.dept_num}, NAME={saved_dept.dept_name}, MANAGER={saved_dept.dept_manager}')
        logger.info('database closes')
        database.close()


def populate_jobs():
    
    logger.info('Working with Job class')
    logger.info('Creating Job records. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPT = 5

    jobs = [
        ('Accountant', '2002-06-14', '2006-08-21', 65000, 'Sharon', 'ACNT'),
        ('PR Manager', '2007-01-30', '2012-09-24', 45000, 'Elizabeth', 'PR01'),
        ('Software Dev', '2012-09-25', '2013-01-10', 50000,'Elizabeth', 'SFTW'),
        ('Karate', '2013-01-11', '2015-06-30', 65000, 'Elizabeth', 'ACNT'),
        ('Strongman', '2015-07-01', '2016-01-29', 75000, 'Elizabeth', 'ENGR'),
        ('Student', '2016-01-30', '2017-04-23', 90000, 'Elizabeth', 'ANAL'),
        ('CEO', '2017-04-24', '2018-06-21', 150000, 'Elizabeth', 'ADMN'),
        ('Engineer', '2008-02-28', '2015-11-08', 75000, 'Emelia', 'ENGR'),
        ('Software', '2005-08-12', '2018-02-01', 80000, 'Brandon', 'SFTW'),
        ('Software Intern', '2012-05-30', '2012-07-21', 30000, 'Shang', 'SFTW'),
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'ANAL'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'ANAL'),
        ('Analyst Manager', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'ANAL'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'ADMN'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'ADMN')
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
                    duration = date_diff_days(job[START_DATE], job[END_DATE]),
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_dept = job[DEPT])
                new_job.save()
                logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('Print the Job records we saved...')
        for saved_job in Job:
            logger.info(f'{saved_job.job_name} | DEPT:{saved_job.job_dept} MANAGER:{saved_job.person_employed} START:{saved_job.start_date} END:{saved_job.end_date} DURATION:{saved_job.duration}')
        logger.info('database closes')
        database.close()


def conv_str_date(date_str):
    #date_str must be in YYYY-MM-DD formate
    ymd = []
    for x in date_str.split('-'):
        ymd.append(int(x))
    return date(*ymd)


def date_diff_days(d1, d2):
    if type(d1) == str:
        d1 = conv_str_date(d1)
    if type(d2) == str:
        d2 = conv_str_date(d2)
    
    return(d2-d1).days

if __name__ == '__main__':
    populate_people()
    populate_departments()
    populate_jobs()
