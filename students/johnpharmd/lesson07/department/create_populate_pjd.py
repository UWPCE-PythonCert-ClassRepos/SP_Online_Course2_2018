"""
    create_pjd.py -- create person/job/department
    Modified from create_personjob.py, credit to UW Python 220
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *
from datetime import date


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in ' +
            'the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('pjd.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

logger.info('This means we can easily switch to a different database')
logger.info('Enable the Peewee magic! This base class does it all')
logger.info('By inheritance only we keep our' +
            'model (almost) technology neutral')


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths,+if mandatory')
    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Now the Job class with a similar approach')
    job_name = CharField(primary_key=True, max_length=30)
    logger.info('Dates')
    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')
    logger.info('Number')

    salary = DecimalField(max_digits=7, decimal_places=2)
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by',
                                      null=False)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of a
        Department we want to research.
    """

    logger.info('And now the Department class also')
    department_name = CharField(primary_key=True, max_length=30)
    logger.info('Letter followed by 3 digits')
    department_number = CharField(max_length=4)
    department_manager_name = CharField(max_length=30)
    logger.info('Which job in the Department')
    job_name = ForeignKeyField(Job, related_name='was_held_by', null=False)
    logger.info('Number of days job was held')
    # days_job_held = IntegerField(null=False)


class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")

    person_name = CharField(max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


def populate_db():
    """
    add person, job, and department data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # database = SqliteDatabase('pjd.db')

    logger.info('Working with Person class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for ' +
                'this from a user')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', 'Painter'),
        ('Susan', 'Boston', 'Beannie'),
        ('Pam', 'Coventry', 'PJ'),
        ('Steven', 'Colchester', None),
        ]

    logger.info('Creating Person records: iterate through the list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

    try:
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name=person[PERSON_NAME],
                        lives_in_town=person[LIVES_IN_TOWN],
                        nickname=person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in ' +
                        f'{saved_person.lives_in_town} ' +
                        f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('Database will now populate jobs')

    logger.info('Working with Job class')
    logger.info('Creating Job records: just like Person. ' +
                'We use the foreign key')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4

    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew'),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew'),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew'),
        ('Admin supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter'),
        ('Admin manager', '2014-11-14', '2018-01-05', 45900, 'Peter')
        ]

    try:
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name=job[JOB_NAME],
                    start_date=job[START_DATE],
                    end_date=job[END_DATE],
                    salary=job[SALARY],
                    person_employed=job[PERSON_EMPLOYED])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            d1_list = [int(n) for n in job.start_date.split('-')]
            date1 = date(d1_list[0], d1_list[1], d1_list[2])
            d2_list = [int(n) for n in job.end_date.split('-')]
            date2 = date(d2_list[0], d2_list[1], d2_list[2])

            delta = abs(date1 - date2)
            logger.info(f'{job.job_name} : {delta.days} days ' +
                        f'for {job.person_employed}')
            # logger.info(f'{job.job_name} : {job.start_date} to ' +
            #             f'{job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    logger.info('Working with Department class')
    logger.info('Creating Department records: just like Job. ' +
                'We use the foreign key')

    DEPARTMENT_NAME = 0
    DEPARTMENT_NUMBER = 1
    DEPARTMENT_MANAGER_NAME = 2
    JOB_NAME = 3
    # DAYS_JOB_HELD = 4

    departments = [
               ('Accounting and Finance', 'A371', 'Mark', 'Analyst'),
               ('Production', 'P593', 'James', 'Senior analyst'),
               ('Marketing', 'M739', 'Jerry', 'Senior business analyst'),
               ('Information Technology', 'I735', 'Eric', 'Admin supervisor'),
               ('Purchasing', 'P175', 'David', 'Admin manager')
               ]

    try:
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                    department_name=department[DEPARTMENT_NAME],
                    department_number=department[DEPARTMENT_NUMBER],
                    department_manager_name=department[DEPARTMENT_MANAGER_NAME],
                    job_name=department[JOB_NAME])
                #     days_job_held=department[DAYS_JOB_HELD])
                new_department.save()

        logger.info('Reading and print all Department rows ' +
                    '(note the value of job)...')
        for department in Department:
            logger.info(f'{department.job_name} : ' +
                        f'{department.job_name.start_date} to ' +
                        f'{department.job_name.end_date}')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_NAME]}')
        logger.info(e)


database.create_tables([
        Job,
        Person,
        Department,
        PersonNumKey
    ])

populate_db()
database.close()
