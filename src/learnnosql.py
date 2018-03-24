
import src.learn_data
import src.mongodb_script
import src.redis_script
import src.neo4j_script
from src.utilities import configure_logger

"""
    learn nosql part 1 : mongodb
    pip install pytest-cov
    py.test -l --pylint --cov tests --showlocals --tb=auto --junitxml=results.xml


log.debug('debug message!')
log.info('info message!')
log.error('error message')
log.critical('critical message')
log.warning('warning message')

log.info("printing from source module")



"""


def showoff_databases():
    """

    """
    log = src.utilities.configure_logger('default', 'logs/nosql_dev.log')
    log.info('Mongodb example uses data from Furniture module, so get it')
    furniture = src.learn_data.get_furniture_data()
    src.mongodb_script.run_example(furniture)

    log.info('All others use data embedded in the modules')

    src.redis_script.run_example()
#    src.neo4j_script.run_example()
#    src.simple_script.run_example()


if __name__ == '__main__':
    """

    """

    showoff_databases()
