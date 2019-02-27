"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('person_job_dept.db')
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

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of a persons
        department.
    """
    logger.info('Department Number')
    dept_number = CharField(primary_key=True, max_length=4, constraints=[
        Check(
            'substr ( dept_number , 1 , 1 ) BETWEEN "A" AND "Z" '
        )
    ])
    logger.info('Department Name')
    dept_name = CharField(max_length=30)
    logger.info('Department Manager')
    dept_manager = CharField(max_length=30, null=False)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    job_name = CharField(primary_key=True, max_length=30)
    logger.info('Dates')
    start_date = DateField(formats="%Y-%m-%d")
    end_date = DateField(formats="%Y-%m-%d")

    duration_days = IntegerField()
    logger.info('Duration_days')
    salary = DecimalField(max_digits=7, decimal_places=2)
    logger.info('Salary')
    logger.info('FOREIGN KEYS: Each job is linked to a peson and a department')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null=False)
    job_department = ForeignKeyField(Department, related_name='in_department', null=False)
    # 'work_department'

database.create_tables([Person, Department, Job])
database.close()
