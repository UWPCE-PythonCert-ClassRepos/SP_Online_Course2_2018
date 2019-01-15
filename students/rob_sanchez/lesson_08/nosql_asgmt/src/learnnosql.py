"""

Integrated example for nosql databases

"""

import learn_data
import new_data
import mongodb_script
import redis_script
import neo4j_script
import simple_script
import utilities


def showoff_databases():
    """
    Here we illustrate basic interaction with nosql databases
    """

    log = utilities.configure_logger('default', '../logs/nosql_dev.log')

    # New furniture data source
    furniture = new_data.get_furniture_data()

    log.info("Running MongoDB exercise")
    mongodb_script.run_example(furniture)

    # log.info("Running Redis exercise")
    # redis_script.run_example()

    # log.info("Running Neo4J exercise")
    # neo4j_script.run_example()

    # log.info("Running persistence and serialization exercise")
    # simple_script.run_example(furniture)


if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    showoff_databases()
