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


database = SqliteDatabase('personjobdept.db')

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
        This class defines Department, which maintains details of the Department
        a Person held a Job in.
    """

    logger.info('Department class')

    logger.info('Define department number')
    department_number = CharField(primary_key=True, max_length=4,
                                  constraints=[Check('substr(department_number,1,1) BETWEEN "A" AND "Z"')])

    logger.info('Define length of department name')
    department_name = CharField(max_length=30)

    logger.info('Define length of department manager name')
    department_manager = CharField(max_length=30)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Now the Job class with a simlar approach')
    job_name = CharField(primary_key = True, max_length = 30)
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    logger.info('Number')

    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    dept_of_job = ForeignKeyField(Department)


class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")

    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

# Data


logger.info('Add data to the database')

people_data = [('Michael', 'Seattle', 'Mike')]
department_data = [('A111','Software Engineering', 'Sam')]
job_data = [('Software Developer', '2011-04-15', '2018-07-03', 165500, 'Michael', 'A111')]

database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')
database.create_tables([
        Job,
        Department,
        Person,
        PersonNumKey
    ])

for x in people_data:
    Person.create(person_name=x[0], lives_in_town=x[1], nickname=x[2])

for x in department_data:
    Department.create(department_number=x[0],
                      department_name=x[1],
                      department_manager=x[2])

for x in job_data:
    Job.create(job_name=x[0],
               start_date=x[1],
               end_date=x[2],
               salary=x[3],
               person_employed=x[4],
               dept_of_job=x[5])

database.close()
