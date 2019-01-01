import logging
from create_personjobdepartment import *
import datetime


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

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000,
         'Andrew'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter')
    ]

    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2
    NAME_OF_JOB = 3

    departments = [
        ('H153', 'Business Intelligence', 'John Phillips', 'Analyst'),
        ('H567', 'Product Development', 'Rose Adams', 'Senior analyst'),
        ('H195', 'Enterprise Strategy', 'Jonathan Range', 'Senior business '
                                                     'analyst'),
        ('K976', 'Production Engineering', 'Kathryn Allen', 'Admin '
                                                            'supervisor'),
        ('L763', 'Reliability Engineering', 'Adam Stunt', 'Admin manager')
    ]

    logger.info('Creating Person and Job records: iterate through the list of '
                'tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name=person[PERSON_NAME],
                        lives_in_town=person[LIVES_IN_TOWN],
                        nickname=person[NICKNAME])
                new_person.save()
                logger.info('Database Person add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in '
                        f'{saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

        for job in jobs:
            date_end = datetime.datetime.strptime(job[END_DATE],"%Y-%m-%d")
            date_start = datetime.datetime.strptime(job[START_DATE],"%Y-%m-%d")
            duration = date_end - date_start
            with database.transaction():
                new_job = Job.create(
                        job_name=job[JOB_NAME],
                        start_date=job[START_DATE],
                        end_date=job[END_DATE],
                        salary=job[SALARY],
                        employment_duration=duration.days,
                        person_employed=job[PERSON_EMPLOYED])
                new_job.save()
                logger.info('Database job add successful')

        logger.info('Print the Job records we saved...')
        for saved_job in Job:
            logger.info(f'{saved_job.person_employed} held the job of '
                        f'{saved_job.job_name} from '
                        f'{saved_job.start_date} to '
                        f'{saved_job.end_date} with a salary of '
                        f'{saved_job.salary}')

        for department in departments:
            with database.transaction():
                new_department = Department.create(
                        department_number=department[DEPARTMENT_NUMBER],
                        department_name=department[DEPARTMENT_NAME],
                        department_manager=department[DEPARTMENT_MANAGER],
                        name_of_job=department[NAME_OF_JOB])
                new_department.save()
                logger.info('Database department add successful')

        logger.info('Print the department records we saved...')
        for saved_department in Department:
            logger.info('Department ' f'{saved_department.department_number} '
                        'is named ' f'{saved_department.department_name}'
                        ', managed by ' 
                        f'{saved_department.department_manager}, and has a '
                        f'job of ' f'{saved_department.name_of_job}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_db()