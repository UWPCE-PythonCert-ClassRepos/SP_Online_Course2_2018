"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

import logging

from personjob_model import *

database = SqliteDatabase('personjob.db')

def add_and_delete():
    """"
        show how we can add a record, and delete a record
    """

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

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

if __name__ == '__main__':
    add_and_delete()