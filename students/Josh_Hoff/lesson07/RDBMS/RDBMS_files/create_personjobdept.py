"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

DATABASE = 'personjob.db'

db = SqliteDatabase(DATABASE)
db.connect()
db.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

logger.info('This means we can easily switch to a different database')
logger.info('Enable the Peewee magic! This base class does it all')
logger.info('By inheritance only we keep our model (almost) technology neutral')

class BaseModel(Model):
    """
        This class is the base model
    """
    class Meta:
        """
            This class is the meta
        """
        database = db

class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)

class Department(BaseModel):
    """
        This class tracks in which Department a Person held a Job.
        For a Department, we need to know it's department number, which is 4 characters long
        and starts with a letter. We need to know the department name (30 characters), and the
        name of the department manager (30 characters). We also need to know the duration in
        days that the job was held. Think about this last one carefully.
    """

    logger.info('A Department class')
    logger.info('Getting the department number')
    department_number = CharField(primary_key=True, max_length=4) #needs to start with a letter
    logger.info('Getting the name of the department')
    department_name = CharField(max_length=30)
    logger.info('Getting the department manager name')
    department_manager = CharField(max_length=30)

class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    person_employed = ForeignKeyField(Person, backref='names', null=False)

    logger.info('Now the Job class with a simlar approach')
    job_name = CharField(primary_key=True, max_length=30)
    logger.info('Dates')
    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')
    logger.info('Duration of Job')
    duration = IntegerField()
    logger.info('Number')
    salary = DecimalField(max_digits=7, decimal_places=2)
    logger.info('Which person had the Job')

    job_dept = ForeignKeyField(Department, backref='in_department', null=False)

class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")

    person_name = CharField(max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)

db.create_tables([
        Job,
        Person,
        PersonNumKey,
        Department
    ])
"""
try:
    wife_tatsiana = Person.create(person_name='Tatsiana',
    lives_in_town='Vancouver', nickname='Tanya')
    tatsiana_job = Job.create(person_employed=wife_tatsiana,
    job_name='Contract_Analyst', start_date=date(2018, 9, 1),
        end_date=date(2018, 10, 1), salary=40000)
    tatsiana_dept = Department.create(department_number='A292',
    department_name='Analyzation_Dept',
        department_manager='Michael', job_length=tatsiana_job)

    for job in Job.select().where(Job.person_employed == wife_tatsiana):
        print(job.start_date)
        print(job.end_date)

except IntegrityError:
    print('not unique')
try:
    sister_melanie = Person.create(person_name='Melanie', lives_in_town='Spokane',
    nickname='Mel')
    mel_job = Job.create(person_employed=sister_melanie,
    job_name='Graphic_Designer', start_date=date(2000, 8, 2),
        end_date=date(2002, 12, 25), salary=30000)

except IntegrityError:
    print('not unique')
try:
    dad_mike = Person.create(person_name='Michael',
    lives_in_town='Colbert', nickname='Mike')
    mike_job1 = Job.create(person_employed=dad_mike,
    job_name='Home_Constructor', start_date=date(1990, 1, 1),
        end_date=date(2012, 1, 1), salary=80000)
    mike_job2 = Job.create(person_employed=dad_mike,
    job_name='Dad', start_date=date(1991, 9, 17),
        end_date=date(2018, 12, 21), salary=0)
    mike_job3 = Job.create(person_employed=dad_mike,
    job_name='Husband', start_date=date(1998, 4, 1),
        end_date=date(2018, 12, 21), salary=0)

except IntegrityError:
    print('not unique')


query = Person.select().order_by(Person.person_name).prefetch(Job)
for person in query:
    print(person.person_name)
    for job in person.names:
        print('  *', job.job_name)

query = Person.select().order_by(Person.person_name).prefetch(Job, Department)
 for person in query:
     print(person.person_name)
     for job in person.names:
         print('  *', job.job_name)
         for dept in job.duration:
             print('    *', dept.department_name)
"""
db.close()
