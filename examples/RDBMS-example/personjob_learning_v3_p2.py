"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from personjob_model import *

import logging

def select_and_update():
    """"
        show how we can select a specific record, and then search and read through several records
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

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

if __name__ == '__main__':
    select_and_update()