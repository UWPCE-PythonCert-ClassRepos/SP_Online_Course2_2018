# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *

#if database:
#    database.drop_tables([Person, Job, Dept])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

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
    
class Dept(BaseModel):
    """
        This class defines a Department, which maintains details for which jobs are in which department and who manages it.
    """

    logger.info('A Department class')
    logger.info("Note: no primary key so we're give one 'for free'")
    
    char_check = ("upper(substr(dept_num, 1, 1)) in "
                 "('A','B','C','D','E','F','G','H','I','J','K','L','M',"
"'N','O','P','Q','R','S','T','U','V','W','X','Y','Z')")
    
#    char_check = ("upper(substr(dept_num, 1, 1)) in map(chr, range(65, 91)")

    dept_num = CharField(primary_key=True, max_length = 4, constraints=[Check(char_check)])
    dept_name = CharField(max_length = 30)
    dept_mgr = CharField(max_length = 30)
    
    
class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Now the Job class with a simlar approach')
    job_name = CharField()#(primary_key = True, max_length = 30)
    
    logger.info('Dates')
    start_date = DateField()#(formats = 'YYYY-MM-DD')
    end_date = DateField()#(formats = 'YYYY-MM-DD')
    job_len = IntegerField()
    
    logger.info('Number')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    
    dept = ForeignKeyField(Dept)

database.create_tables([Person, Dept, PersonNumKey, Job])

database.close()