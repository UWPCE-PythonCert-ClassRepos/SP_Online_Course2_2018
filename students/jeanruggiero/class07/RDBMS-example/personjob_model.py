"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema

"""

from peewee import *
import logging
import datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Create database.')
database = SqliteDatabase('job_history.db', pragmas={'foreign_keys': 1})
database.connect()

logger.info('Define the schema for the database.')


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Define the Person model.')
    logger.info('Specify the fields in our model and their lengths.')
    logger.info('Use the person name as the unique identifier for a person.')
    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)

    logger.info('Nickname is an optional field.')
    nickname = CharField(max_length=20, null=True)


class Department(BaseModel):
    """
    This class defines Department, which maintains details of which jobs
    belong in each department.
    """
    logger.info('Define the Department model.')
    logger.info('Specify the fields in our model and their lengths.')

    logger.info('Department number is the unique identifier for each department.')
    logger.info('Enforce that the department_number be exactly 4 characters long and start with a letter.')
    department_number = CharField(primary_key=True, constraints=[
        Check("department_number GLOB '[a-zA-Z]*'"),
        Check("length(department_number) == 4")
        ])

    logger.info('Define department name and manager.')
    department_name = CharField(max_length=30)
    department_manager = CharField(max_length=30)



class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Define the Job model.')
    logger.info('Specify the fields in our model and their lengths.')

    logger.info('Use job_name as unique identifier.')
    job_name = CharField(primary_key=True, max_length=30)

    logger.info('Use date fields to specify job start and end dates.')
    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')

    salary = DecimalField(max_digits=7, decimal_places=2)

    logger.info('Use ForeignKeyFields to link the job to a person and to a department.')
    logger.info('Each job may be filled by one and only one person and belong to one and only one department.')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null=False)
    job_department = ForeignKeyField(Department, related_name="is_in_department", null=False)

    logger.info('Use a property to calculate the duration in days the job was held.')

    @property
    def job_length(self):
        """
        Return the duration in days the job was held.
        """
        return (datetime.date.fromisoformat(self.end_date) - datetime.date.fromisoformat(self.start_date)).days


logger.info('Adding Job, Department, and Person tables to job_history.db')
database.create_tables([Job, Person, Department])
database.close()
