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
database.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    job_name = CharField(primary_key=True, max_length=30)
    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')
    salary = DecimalField(max_digits=7, decimal_places=2)
    person_employed = ForeignKeyField(Person,
                                      related_name='was_filled_by',
                                      null=False)


class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    person_name = CharField(max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of past
        department_names and corresponding department details.
    """
    dept_number = CharField(max_length=4)
    dept_name = CharField(max_length=30)
    dept_manager = CharField(max_length=30)
    job_name = ForeignKeyField(Job, null=False)  # Job name is a
    # primary key in the Job Table and so can be used as
    # foreign key. There is no need to have employee name in this table
    # since job_name is unique and points back to Person table with a
    # foreign key.
    days_held = CharField(null=True)
