from create_personjobdepartment import *

import logging

def populate_persons():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_department.db')

    logger.info('Working with Person class')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Andrew', 'Boston', 'Andy'),
        ('Peter', 'Seattle', 'Pete'),
        ('Danielle', 'Seattle', 'Dani'),
        ('Drew', 'Boston', 'Dre'),
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


def populate_departments():
    """
        add department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_department.db')

    logger.info('Working with Department class')

    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2

    departments = [
        ('B100', 'Business Metrics Analysis' , 'Danielle'),
        ('D100', 'Database Administration' , 'Peter')
    ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    department_number = department[DEPARTMENT_NUMBER],
                    department_name = department[DEPARTMENT_NAME],
                    department_manager = department[DEPARTMENT_MANAGER])
                new_department.save()

        logger.info('Reading and print all Department rows (note the value of manager)...')
        for department in Department:
            logger.info('Dept. number: {}, Dept. name: {}, Dept. manager: {}'\
                        .format(department.department_number, department.department_name, department.department_manager))

    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_NUMBER]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


def populate_jobs():
    """
        add job data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('person_job_department.db')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    JOB_DEPARTMENT = 4
    PERSON_EMPLOYED = 5

    jobs = [
        ('Business Analyst', '2001-09-22', '2003-01-30', 65500, 'B100', 'Andrew'),
        ('Senior Business Analyst', '2003-02-01', '2006-10-22', 77500, 'B100', 'Andrew'),
        ('Business Analyst Manager', '2001-01-01', '2008-01-30', 96500, 'B100', 'Danielle'),
        ('DB Admin', '2001-10-01', '2004-09-28', 68900, 'D100', 'Drew'),
        ('Senior DB Admin', '2004-10-01', '2006-11-10', 80000, 'D100', 'Drew'),
        ('DB Admin supervisor', '2002-10-01', '2004-11-10', 86900, 'D100', 'Peter'),
        ('DB Admin manager', '2004-11-14', '2008-01-05', 100000, 'D100', 'Peter')
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
                    department = job[JOB_DEPARTMENT],
                    person_employed = job[PERSON_EMPLOYED])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()


if __name__ == '__main__':
    populate_persons()
    populate_departments()
    populate_jobs()
