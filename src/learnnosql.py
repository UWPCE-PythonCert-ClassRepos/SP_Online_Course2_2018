"""

Integrated example for nosql databases

"""

import src.learn_data
import src.mongodb_script
import src.redis_script
import src.neo4j_script
import src.simple_script
import src.utilities


def showoff_databases():
    """
    Here we illustrate basic interaction with nosql databases
    """

    log = src.utilities.configure_logger('default', 'logs/nosql_dev.log')

    log.info("Mongodb example use data from Furniture module, so get it")
    furniture = src.learn_data.get_furniture_data()

    src.mongodb_script.run_example(furniture)

    log.info("Other databases use data embedded in the modules")

    src.redis_script.run_example()
    src.neo4j_script.run_example()
    src.simple_script.run_example(furniture)


if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    showoff_databases()
