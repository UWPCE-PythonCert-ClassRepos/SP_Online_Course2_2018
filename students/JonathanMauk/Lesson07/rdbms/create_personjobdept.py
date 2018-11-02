"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjobdept.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only

logger.info('This means we can easily switch to a different database')
logger.info('Enable the Peewee magic! This base class does it all')
logger.info('By inheritance only we keep our model (almost) technology neutral')


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths and if mandatory.')
    logger.info('Must be a unique identifier for each person.')

    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Now the Job class with a similar approach.')
    job_name = CharField(primary_key=True, max_length=30)
    logger.info('Dates.')
    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')
    logger.info('Number.')
    duration = IntegerField()
    logger.info('Duration of job.')

    salary = DecimalField(max_digits=7, decimal_places=2)
    logger.info('Which person had the Job.')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null=False)
    job_dept = ForeignKeyField(Department, related_name='in_department', null=False)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of which
        Departments a person has worked under.
    """

    logger.info('Now the Department class.')
    dept_number = CharField(primary_key=True, max_length=4)
    logger.info('Department number.')
    dept_name = CharField(max_length=30, null=False)
    logger.info('Department name.')
    dept_manager = CharField(max_length=30, null=False)
    logger.info('Department manager.')



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


database.create_tables([
        Job,
        Person,
        PersonNumKey
    ])

database.close()
