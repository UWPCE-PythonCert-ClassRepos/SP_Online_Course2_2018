"""
    learn nosql part 1 : mongodb
    pip install pytest-cov
    py.test -l --pylint --cov tests --showlocals --tb=auto --junitxml=results.xml

"""

import logging
import logging.config
import learn_data
import mongodb_script
import redis_script
import neo4j_script


#from simple_script import run_simple

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,  # stop neo4j driver from being noisy!
    'loggers': {
        '': {
            'level': 'INFO',
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)


def showoff_databases():
    """

    """

    logging.info('Mongodb example uses data from Furniture module, so get it')
    furniture = learn_data.get_furniture_data()
    mongodb_script.run_example(furniture)

    logging.info('All others use data embedded in the modules')

    redis_script.run_example()
    neo4j_script.run_example()
    simple_script.run_example()


if __name__ == '__main__':
    """

    """

    showoff_databases()
