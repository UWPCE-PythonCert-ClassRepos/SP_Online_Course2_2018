"""
    Assignment 1: Create the database table format
    Simple database example with Peewee ORM, sqlite and Python
    Here we definethe schema
    Use logging for messages so that they can be turned off
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_key = ON;')

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

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique indentifier for each person')

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


class Department(BaseModel):
    """
        Assignment 1 adding character field for department
    """

    logger.info('Now the Department class with a similar approach')
    logger.info('Department Number')
    department_id = CharField(primary_key = True, max_length = 4)
    logger.info('Department Name')
    department_name = CharField(max_length = 30)
    logger.info('Department Manager')
    department_manager = CharField(max_length = 30)
    #logger.info('StartDate and EndDate')
    #start_date_department = DateField(formats = 'YYYY-MM-DD')
    #end_date_department = DateField(formats = 'YYYY-MM_DD')
    #logger.info('Duration')
    #duration = end_date - start_date


class Job(BaseModel):
    """
        This class defines Jon, which maintains details of past Jobs
        held by a Person
    """

    logger.info('Now the Job class with a similar approach')
    job_name = CharField(primary_key = True, max_length = 30)
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM_DD')
    duration = IntegerField()
    logger.info('Number')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Which person had the job')
    person_employed = ForeignKeyField(Person, related_name = 'was_filled_by', null = False)
    department_id = ForeignKeyField(Department, related_name = 'was_filled_by', null=False)


class PersonNumKey(BaseModel):

    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")

    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


logger.info('Create the table format')
database.create_tables([
        Job,
        Person,
        PersonNumKey,
        Department])
database.close()
