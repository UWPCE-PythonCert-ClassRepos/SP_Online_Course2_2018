"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
import os
from peewee import *

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Department(BaseModel):
    """
        Department Class: defines the department in which a person held a job.
        Need to know:
          1. Department number - 4 char and starts with letter
          2. Department name - 30 char
          3. Department manager name - 30 char
          4. Duration the job was held (in Job class)
    """
    logger.debug('Creating department class - dept num, name, manager name.')
    logger.debug("Department Number is Primary Key")
    department_number = CharField(primary_key=True, max_length=4, 
    constraints=[Check('upper(substr(department_number, 1, 1) BETWEEN "A" and "Z" )')])
    department_name = CharField(max_length=30)
    department_manager = CharField(max_length=30)


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.

        Added the time spent in job.
    """

    logger.info('Now the Job class with a simlar approach')
    job_name = CharField(primary_key = True, max_length = 30)
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    logger.debug('Adding duration field)')
    job_duration = IntegerField()
    logger.info('Number')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    logger.debug('Adding job department foreign key to tie job to department.  Person already tied to job')
    job_department = ForeignKeyField(Department, related_name='in_department', null=False)


class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")

    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

try: 
    logger.debug("Creating database.")
    database.create_tables([
            Job,
            Department,
            Person,
            PersonNumKey
        ])
    logger.debug("Database created.")

# Remove existing DB
except Exception as ex:
    logger.error("Unable to create database.  Dropping existing db.")
    database.close()
    os.remove('personjob.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    database.create_tables([
            Job,
            Department,
            Person,
            PersonNumKey
        ])
    logger.debug("Database created.")
finally:
    database.close()