'''
runs all personjob_learning steps
'''

import logging

from personjobdepartment_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    '''creates database tables'''
    database = SqliteDatabase('personjob.db')
    try:
        database.connect()
        logger.info('Creating tables in database')
        database.create_tables([
            Job,
            Person,
            PersonNumKey,
            Department
        ])
        database.close()
    except Exception as e:
        logger.info(e)

def populate_db():
    """
    add person data to database
    """

    database = SqliteDatabase('personjob.db')

    logger.info('Working with Person class')
    logger.info('Note how I use constants and a list of tuples as a simple schema')
    logger.info('Normally you probably will have prompted for this from a user')

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

    logger.info('Creating Person records: iterate through the list of tuples')
    logger.info('Prepare to explain any errors with exceptions')
    logger.info('and the transaction tells the database to fail on error')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for person in people:
            with database.transaction():
                new_person = Person.create(
                        person_name = person[PERSON_NAME],
                        lives_in_town = person[LIVES_IN_TOWN],
                        nickname = person[NICKNAME])
                new_person.save()
                logger.info('Database add successful')

        logger.info('Print the Person records we saved...')
        for saved_person in Person:
            logger.info(f'{saved_person.person_name} lives in {saved_person.lives_in_town} ' +\
                f'and likes to be known as {saved_person.nickname}')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

    finally:
        logger.info('database closes')
        database.close()

def select_and_update():
    """"
        show how we can select a specific record, and then search and read through several records
    """

    database = SqliteDatabase('personjob.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info('Find and display by selecting a spcific Person name...')
        aperson = Person.get(Person.person_name == 'Susan')

        logger.info(f'{aperson.person_name} lives in {aperson.lives_in_town} ' + \
        f' and likes to be known as {aperson.nickname}')

        logger.info('Search and display all Person with missing nicknames')
        logger.info('Our person class inherits select(). Specify search with .where()')
        logger.info('Peter gets a nickname but noone else')

        for person in Person.select().where(Person.nickname == None):
            logger.info(f'{person.person_name} does not have a nickname; see: {person.nickname}')
            if person.person_name == 'Peter':
                logger.info('Changing nickname for Peter')
                logger.info('Update the database')
                person.nickname = 'Painter'
                person.save()
            else:
                logger.info(f'Not giving a nickname to {person.person_name}')

        logger.info('And here is where we prove it by finding Peter and displaying')
        aperson = Person.get(Person.person_name == 'Peter')
        logger.info(f'{aperson.person_name} now has a nickname of {aperson.nickname}')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

def add_and_delete():
    """"
        show how we can add a record, and delete a record
    """
    database = SqliteDatabase('personjob.db')
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        logger.info('Add and display a Person called Fred; then delete him...')
        logger.info('Add Fred in one step')

        new_person = Person.create(
            person_name = 'Fred',
            lives_in_town = 'Seattle',
            nickname = 'Fearless')
        new_person.save()

        logger.info('Show Fred')
        aperson = Person.get(Person.person_name == 'Fred')

        logger.info(f'We just created {aperson.person_name}, who lives in {aperson.lives_in_town}')
        logger.info('but now we will delete him...')

        aperson.delete_instance()

        logger.info('Reading and print all Person records (but not Fred; he has been deleted)...')

        for person in Person:
            logger.info(f'{person.person_name} lives in {person.lives_in_town} and likes to be known as {person.nickname}')

    except Exception as e:
        logger.info(e)

    finally:
        database.close()

def populatejob_db():
    """
        add job data to database
    """

    database = SqliteDatabase('personjob.db')

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    SALARY = 3
    PERSON_EMPLOYED = 4
    JOB_DEPARTMENT = 5

    logger.info('Added job_department values as all Null')
    jobs = [
        ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew',None),
        ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew',None),
        ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew',None),
        ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter',None),
        ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter',None)
        ]

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for job in jobs:
            with database.transaction():
                new_job = Job.create(
                    job_name = job[JOB_NAME],
                    start_date = job[START_DATE],
                    end_date = job[END_DATE],
                    salary = job[SALARY],
                    person_employed = job[PERSON_EMPLOYED],
                    job_department = job[JOB_DEPARTMENT])
                new_job.save()

        logger.info('Reading and print all Job rows (note the value of person)...')
        for job in Job:
            logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

    finally:
        logger.info('database closes')
        database.close()

if __name__ == '__main__':
    create_tables()
    populate_db()
    select_and_update()
    add_and_delete()
    populatejob_db()