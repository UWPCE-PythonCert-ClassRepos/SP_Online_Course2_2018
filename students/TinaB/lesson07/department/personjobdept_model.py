"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema
    Add log statements to explain whats happening

"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjobdept.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')

# if you wanted to use heroku postgres:
#
# psycopg2
#
# parse.uses_netloc.append("postgres")
# url = parse.urlparse(os.environ["DATABASE_URL"])
#
# conn = psycopg2.connect(
# database=url.path[1:],
# user=url.username,
# password=url.password,
# host=url.hostname,
# port=url.port
# )
# database = conn.cursor()
#
# Also consider elephantsql.com (be sure to use configparser for PWß)

logger.info('This means we can easily switch to a different database')

logger.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    class Meta:
        database = database
logger.info('By inheritance only we keep our model (almost) technology neutral')


class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info(
        'Specify the fields in our model, their lengths and if mandatory')
    logger.info('Creating Person Class, with field definitions')
    logger.info('Must be a unique identifier for each person')

    logger.info('Person Name')
    person_name = CharField(primary_key=True, max_length=30)

    logger.info('Lives in Town')
    lives_in_town = CharField(max_length=40)

    logger.info('Nickname')
    nickname = CharField(max_length=20, null=True)


class Department(BaseModel):
    """
        This class defines Department, which maintains details of the
        Departments that jobs are in.
    """

    logger.info('Creating Department Class, with field definitions')

    logger.info('Department Number')
    department_number = CharField(primary_key=True, max_length=4, constraints=[
        Check(
            'upper ( substr ( department_number , 1 , 1 ) BETWEEN "A" AND "Z" )'
        )
    ])
    logger.info('Department Name')
    department_name = CharField(max_length=30)

    logger.info('Department Manager')
    department_manager = CharField(max_length=30, null=False)


class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    logger.info('Creating Job Class, with field definitions')
    logger.info('Job Name')
    job_name = CharField(primary_key=True, max_length=30)

    logger.info('Start Date')
    start_date = DateField(formats='YYYY-MM-DD')

    logger.info('End Date')
    end_date = DateField(formats='YYYY-MM-DD')

    logger.info('Duration of job')
    duration = IntegerField()

    logger.info('Salary')
    salary = DecimalField(max_digits=7, decimal_places=2)

    logger.info('Which person had this job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null=False)

    logger.info('which department this job was in')
    job_department = ForeignKeyField(Department, related_name='in_department', null=False)




database.create_tables([Person, Department, Job])
database.close()
