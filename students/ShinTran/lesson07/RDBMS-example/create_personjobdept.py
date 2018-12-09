"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""


import logging
from peewee import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjobdept.db')
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

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    job_name = CharField(primary_key = True, max_length = 30)
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    logger.info('Number')

    duration = IntegerField()

    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    department_name = CharField(max_length = 30)


class Department(BaseModel):
    """
        This class defines the Department, maintains dept number,
        dept name, dept manager, duration job was held.
    """

    logger.info('Define a department class, a classification for jobs')
    logger.info('Dept ID is 4 characters, start with a letter')

    department_id = CharField(primary_key = True, max_length = 4, constraints = [
        Check('upper(substr(department_id,1,1) BETWEEN "A" AND "Z")')])
    department_name = CharField(max_length = 30)
    department_manager = CharField(max_length = 30, null = False)


database.create_tables([
        Job,
        Person,
        Department])

database.close()
