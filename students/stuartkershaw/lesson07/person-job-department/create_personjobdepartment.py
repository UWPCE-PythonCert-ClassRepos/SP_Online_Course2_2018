"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema

"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('person_job_department.db')
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
    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of the department
        for which each job belonged.
    """
    logger.info('Department number is a unique value and suitable Primary Key.')
    department_number = CharField(primary_key = True, max_length = 4)
    logger.info('Department name is a unique value.')
    department_name = CharField(unique = True, max_length = 30)
    logger.info('Department manager is a foreign key of Person.')
    department_manager = ForeignKeyField(Person, null = False)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    job_name = CharField(primary_key = True, max_length = 30)
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Job department is a foreign key of Department.')
    department = ForeignKeyField(Department, null = False)
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)


database.create_tables([
        Person,
        Department,
        Job
    ])

database.close()