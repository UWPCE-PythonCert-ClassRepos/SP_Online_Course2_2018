"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from personjob_model import *
import logging

def show_integrity_del():
    """
        demonstrate how database protects data inegrity : delete
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    database = SqliteDatabase('personjob.db')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Try to Delete a person who has jobs...')
        with database.transaction():
            aperson = Person.get(Person.person_name == 'Andrew')
            logger.info(f'Trying to delete {aperson.person_name} who lives in {aperson.lives_in_town}')
            aperson.delete_instance()

    except Exception as e:
        logger.info('Delete failed because Andrew has Jobs')
        logger.info(f'Delete failed: {aperson.person_name}')
        logger.info(e)

    finally:
        database.close()

if __name__ == '__main__':
    show_integrity_del()