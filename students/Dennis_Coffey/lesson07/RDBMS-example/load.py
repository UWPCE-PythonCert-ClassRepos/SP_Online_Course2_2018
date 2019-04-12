# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 21:11:33 2019

Load personjob database with person, job and department data

@author: dennis
"""

from create_personjob import *
from datetime import datetime
from peewee import *
import logging
import pprint

database = SqliteDatabase('personjob.db')

def populate_people():
    """
    Add people data to the database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Working with Person class')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2
    
    # List of people to load into database
    people = [('Dennis', 'Woodinville', None),
              ('William', 'Boston', 'Billie'),
              ('Jennifer', 'Kona', 'Jenny'),
              ('Frederick', 'Seattle', 'Freddie'),
              ('Lisa', 'Missoula', None)]
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        # Loop through people list and insert into database
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name = person[PERSON_NAME],
                        lives_in_town = person[LIVES_IN_TOWN],
                        nickname = person[NICKNAME])
                new_person.save()
        logger.info('Reading and print all person rows ...')
        for person in Person:
            logger.info(f'Created {person.person_name} who lives in ' +
                        f'{person.lives_in_town} and goes by the nickname' +
                        f'{person.nickname}')
            
    except Exception as e:
        logger.info(f'Error creating {person[PERSON_NAME]} in database')
        logger.info(e)
        
    finally:
        logger.info('Database closes')
        database.close()

def populate_jobs():
    """
    Add jobs data to the database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Working with Job class')
 
    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    # List of people to load into database
    jobs = [('Sales Manager', '2010-05-31', '2014-08-15', 145000, 'Dennis', 'D002'),
            ('Analyst', '2014-10-31', '2017-06-15', 165000, 'Dennis', 'D001'),
            ('Developer', '2008-03-01', '2016-04-15', 103000, 'Dennis', 'D003'),
            ('Business Analyst', '2010-05-31', '2014-08-15', 65000, 'William', 'D001'),
            ('Program Manager', '2010-05-31', '2014-08-15', 125000, 'William', 'D003'),
            ('Salesman', '2010-05-31', '2014-08-15', 88000, 'Frederick', 'D002'),
            ('Cashier', '2010-05-31', '2014-08-15', 34000, 'Frederick', 'D002'),
            ('Product Owner', '2010-05-31', '2014-08-15', 110000, 'Lisa', 'D003'),
            ('Database Architect', '2010-05-31', '2014-08-15', 165000, 'Jennifer', 'D003'),
            ('Dev Ops', '2010-05-31', '2014-08-15', 104000, 'Jennifer', 'D003'),
            ('Mechanic', '2010-05-31', '2014-08-15', 45000, 'Frederick', 'D004'),
            ('Systems Engineer', '2010-05-31', '2014-08-15', 80000, 'Dennis', 'D001')]
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        # Loop through people list and insert into database
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                        job_name = job[JOB_NAME],
                        start_date = job[START_DATE],
                        end_date = job[END_DATE],
                        salary = job[SALARY],
                        person_employed = job[PERSON_EMPLOYED],
                        department = job[DEPARTMENT])
                new_job.save()

        logger.info('Reading and print all job rows ...')
        for job in Job:
            logger.info(f'{job.job_name}: {job.start_date} to {job.end_date} for {job.person_employed}')
            
    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]} in database')
        logger.info(e)
        
    finally:
        logger.info('Database closes')
        database.close()

def populate_departments():
    """
    Add department data to the database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Working with Department class')

    DEPARTMENT_NUMBER = 0
    DEPARTMENT_NAME = 1
    DEPARTMENT_MANAGER = 2
    
    # List of people to load into database
    departments = [('D001', 'Analysts', 'John Data'),
                  ('D002', 'Sales', 'Sarah Cell'),
                  ('D003', 'IT', 'Isaac Tarantino'),
                  ('D004', 'Automotive', 'Chevy Chase')]
    
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        # Loop through departments list and insert into database
        for department in departments:
            with database.transaction():
                new_department = Department.create(
                        department_number = department[DEPARTMENT_NUMBER],
                        department_name = department[DEPARTMENT_NAME],
                        department_manager = department[DEPARTMENT_MANAGER])
                new_department.save()
                
        logger.info('Reading and print all department rows ...')
        for department in Department:
            logger.info(f'Created {department.department_name} managed by ' +
                        f'{department.department_manager}')
            
    except Exception as e:
        logger.info(f'Error creating {department[DEPARTMENT_NAME]} in database')
        logger.info(e)
        
    finally:
        logger.info('Database closes')
        database.close()

def print_person_list():
    """
    Pretty print that shows all of the departments a
    person worked in for every job they ever had
    """
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    dbdata = Job.select(Job.person_employed).distinct()
    for names in dbdata:
        print("\nEmployee: {}".format(str(names.person_employed)))
        query = (Job.select(Person.person_name, Department.department_name, Department.department_number, Job.job_name,
                            Job.start_date, Job.end_date).join(Person, on=(Person.person_name == Job.person_employed))
                 .join(Department, on=(Department.department_number == Job.department))
                 .where(Person.person_name == names.person_employed).namedtuples())

        for row in query:
            output = [row.job_name, row.department_number, row.department_name]
            pprint.pprint(output)

if __name__ == '__main__':
    # Load people into database
    populate_people()
    # Load jobs into database
    populate_jobs()
    # Load departments into database
    populate_departments()
    # List using pretty print that shows all of the departments a person
    # worked in for every job they ever had
    print_person_list()
