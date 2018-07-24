"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
import datetime
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjobdept.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

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
    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


class Department(BaseModel):
    """
    This class defines Department, which contains its 
    Number:  4 characters long and start with a letter
    Name: 30 characters 
    Manager: Foreign Key Person
    Current manager employed length: Integer
    """
    logger.info('The Department model')

    logger.info('The department number')

    num_check = ("upper(substr(dept_num, 1, 1)) in "
                 "('A','B','C','D','E','F','G','H','I','J','K','L','M',"
                 "'N','O','P','Q','R','S','T','U','V','W','X','Y','Z')")
    
    dept_num = CharField(primary_key=True, max_length=4, unique=True,
                         constraints=[Check(num_check)])

    logger.info('The department name')
    dept_name = CharField(max_length=30)

    logger.info('The manager of the department')
    dept_manager = ForeignKeyField(model=Person, field='person_name')


class Job(BaseModel):
    """
    This class defines Job, which maintains details of past Jobs
    held by a Person.
    """

    logger.info('Now the Job class with a simlar approach')
    job_name = CharField(primary_key=True, max_length=30)
     
    logger.info('Dates')
    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')
    duration = IntegerField()

    logger.info('Number')
    salary = DecimalField(max_digits=7, decimal_places=2)
    
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by',
                                      backref="jobs")
    logger.info('The department the job is in')
    job_dept = ForeignKeyField(Department, backref="jobs")
   

class PersonNumKey(BaseModel):
    """
    This class defines Person, which maintains details of someone
    for whom we want to research career to date.
    """

    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're given one 'for free'")

    person_name = CharField(max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


if __name__ == '__main__':
    logger.info('Creating the tables in PersonJob.db')
    with database as db:
        db.create_tables([
            Job,
            Person,
            Department,
            PersonNumKey
        ])
