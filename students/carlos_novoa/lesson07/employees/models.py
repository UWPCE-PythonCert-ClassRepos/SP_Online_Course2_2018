"""
Employees models
"""

from peewee import *  # noqa F403
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('staff.db')  # noqa F403
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')


class BaseModel(Model):  # noqa F403
    class Meta:
        database = database


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('Define Person model')
    person_name = CharField(primary_key=True, max_length=30)  # noqa F403
    lives_in_town = CharField(max_length = 40)  # noqa F403
    nickname = CharField(max_length=20, null=True)  # noqa F403


class Department(BaseModel):  # noqa F403
    """
        This class defines Department, which maintains past details
        upon which Department a person has worked
    """
    logger.info('Define Department model')
    department_number = CharField(primary_key=True, max_length=4)  # noqa F403
    department_name = CharField(max_length=30)  # noqa F403
    department_manager = CharField(max_length=30)  # noqa F403


class Job(BaseModel):  # noqa F403
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    logger.info('Define Job model')
    job_name = CharField(primary_key=True, max_length=30)  # noqa F403
    start_date = DateField(formats='YYYY-MM-DD')  # noqa F403
    end_date = DateField(formats='YYYY-MM-DD')  # noqa F403
    salary = DecimalField(max_digits=7, decimal_places=2)  # noqa F403
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null=False)  # noqa F403
    in_department =  ForeignKeyField(Department, related_name='department_num', null=False)  # noqa F403
