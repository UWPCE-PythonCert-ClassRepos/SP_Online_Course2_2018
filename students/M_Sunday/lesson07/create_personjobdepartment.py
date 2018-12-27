import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjob.db')
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

    logger.info('Note how we defined the class')

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

    logger.info('Now the Job class with a similar approach')
    logger.info('Creating job name')
    job_name = CharField(primary_key = True, max_length = 30)
    logger.info('Creating start and end dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    logger.info('Creating employment duration')
    employment_duration = DecimalField(max_digits=5, decimal_places = 0)
    logger.info('Creating salary')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Which person had the Job')
    person_employed = CharField(max_length=30)
    # person_employed = ForeignKeyField(Person, related_name='was_filled_by',
    #  null = False)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of the
        department in which someone works.
    """

    logger.info('An alternate Department class')
    logger.info("Note: no primary key so we're give one 'for free'")

    logger.info('Creating a department number')
    department_number = CharField(max_length = 4)
    logger.info('Creating department name')
    department_name = CharField(max_length = 30)
    logger.info('Creating department manager')
    department_manager = CharField(max_length=30)
    logger.info('Creating job name')
    name_of_job = CharField(max_length=30)


database.create_tables([
        Job,
        Person,
        Department
    ])

database.close()
