# Lesson 07 RDBMS exercise
# Base code from RDBMS example from website
# !/usr/bin/env python3


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
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):
    class Meta:
        database = database

class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

class Department(BaseModel):
    """
        This class defines Department, which contains details of the
        Department in which each Job resides.
    """
    
    logger.info('The Department Number is max 4 characters, must start with a letter')
    dept_number = CharField(primary_key = True, max_length = 4, 
                            constraints=[Check('upper( substr( dept_number, 1, 1 ) BETWEEN "A" AND "Z" )')])
    dept_name = CharField(max_length = 30)
    dept_manager = CharField(max_length = 30)

class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Job class has foreign keys of Person and Department')
    job_name = CharField(primary_key = True, max_length = 30)
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    
    person_employed = ForeignKeyField(Person, related_name ='was_filled_by', null = False)
    job_dept = ForeignKeyField(Department, related_name = 'managing_department', null = False)



database.create_tables([
        Person,
        Department,
        Job
    ])

database.close()

