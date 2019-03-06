"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


class Department(BaseModel):
    """
        This class defines Department and maintains department number,
        department name, name of the manager and duration of a job.
    """

    logger.info('The Department class to define department')
    logger.info("Department number")
    dept_number = CharField(primary_key = True, max_length = 4)
    logger.info("Department Name")
    dept_name = CharField(max_length = 30)
    logger.info("Name of Manager")
    manager = CharField(max_length = 30)
    


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    job_name = CharField(primary_key = True, max_length = 30)
    start_date = DateField(formats = 'YYYY-MM-DD') 
    end_date = DateField(formats = 'YYYY-MM-DD')   
    salary = DecimalField(max_digits = 7, decimal_places = 2)  
    person_employed = ForeignKeyField(Person, related_name = 'filled by', null = False)
    logger.info('Job Department')
    job_department_numb = ForeignKeyField(Department, related_name = 'departments', null = False)
    logger.info('Job Duration')
    job_duration = IntegerField()


class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

database.create_tables([
        Person,
        Department,
        Job,
        PersonNumKey
    ])

database.close()
