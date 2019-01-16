"""
    This module defines the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('personjobdept.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

logger.info('Checkpoint: Loading')


class BaseModel(Model):
    class Meta:
        database = database

        
class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Checkpoint: Defining Person class')
    
    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)
    
    logger.info('Checkpoint: Person class processed')

    
class Department(BaseModel):
    
    logger.info('Checkpoint: Defining Department class')
    
    # Verifies that the first value of the department number is a character
    dept_num = CharField(constraints=[Check('lower(substr(Department.dept_num,1,1)) BETWEEN "a" AND "z"')], max_length = 4)
    dept_name = CharField(primary_key = True, max_length = 30)
    dept_manager = CharField(max_length = 30)
    
#    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    
    logger.info('Checkpoint: Department class processed')  
    
    
class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Checkpoint: Defining Job class')
    
    job_name = CharField(primary_key = True, max_length = 30)
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    dept_employed = ForeignKeyField(Department, null = False)
    logger.info('Checkpoint: Job class processed')    

    
# Keeping this dummy for possible future reference
class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """

    logger.info('Checkpoint: Defining alternate Person class - No applicable')

    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)
    logger.info('Checkpoint: Alternate Person class processed')   

# This is to establish the schema in its initial run, but for data structure reference when imported
if __name__ == '__main__':
    database.create_tables([
            Job,
            Department,
            Person,
            PersonNumKey
        ])
    database.close()
