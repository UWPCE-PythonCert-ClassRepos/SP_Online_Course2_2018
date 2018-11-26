"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""
import logging
from work_db_model import *
from datetime import datetime


def populate_db():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('work.db')

    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2

    people = [
        ('Andrew', 'Sumner', 'Andy'),
        ('Peter', 'Seattle', None),
        ('Susan', 'Boston', 'Beannie'),
        ('Pam', 'Coventry', 'PJ'),
        ('Steven', 'Colchester', None),
        ]

    DEPT_NAME = 0
    DEPT_MANAGER = 1
    DEPT_NUMBER = 2

    departments = [
        ('Plumbing', 'Dave', 'P100'),
        ('Sanitation', 'Ernie', 'S100'),
        ('Landscaping', 'Linda', 'L100'),
        ('Lighting', 'Earl', 'L200'),
        ('Production', 'Steve', 'P200'),
        ]

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    DEPARTMENT = 5

    jobs = [('Plumber Apprentice', '2016-01-01', '2018-12-31', 32000,
             'Andrew', 'Plumbing'),
            ('Industrial Engineer', '2003-02-01', '2006-10-22', 24000,
             'Peter', 'Sanitation'),
            ('Mower', '2006-10-23', '2016-12-24', 28000, 'Susan',
             'Landscaping'),
            ('Grip', '2012-10-01', '2014-11-10', 43000, 'Pam',
             'Lighting'),
            ('Editor', '2014-11-14', '2018-01-05', 110000, 'Steven',
             'Production')
            ]


    try:
        logger.info('Connecting to database to add records')
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        database.create_tables([
            Department,
            Job,
            Person,
            PersonNumKey
        ])

        logger.info("Adding persons to database")
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name = person[PERSON_NAME],
                        lives_in_town = person[LIVES_IN_TOWN],
                        nickname = person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        logger.info("Add departments to database")
        for dept in departments:
            Department.create(dept_name=dept[DEPT_NAME],
                              dept_manager=dept[DEPT_MANAGER],
                              dept_number=dept[DEPT_NUMBER])

        logger.info("Adding jobs to database")
        for job in jobs:
            start = datetime.strptime(job[START_DATE],'%Y-%m-%d')
            end = datetime.strptime(job[END_DATE],'%Y-%m-%d')
            duration = end - start
            Job.create(job_name=job[JOB_NAME],
                       start_date=job[START_DATE],
                       end_date=job[END_DATE],
                       duration_days=duration.days,
                       salary=job[SALARY],
                       person_employed=job[PERSON_EMPLOYED],
                       dept_name=job[DEPARTMENT])

    except Exception as e:
        logger.info('Error adding record to database')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    populate_db()
