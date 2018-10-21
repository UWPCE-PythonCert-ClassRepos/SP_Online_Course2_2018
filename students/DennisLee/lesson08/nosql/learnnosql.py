"""
Integrated example for nosql databases
"""
import login_database
import learn_data
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

    log.info(
        "\n\n\nMongodb example to use data from Furniture module, so get it.")
    furniture = learn_data.get_furniture_data()

    log.info("\n\n\nHere's the MongoDB script.")
    mongodb_script.run_example(furniture)

    log.info("Other databases use data embedded in the modules")

    log.info("\n\n\nHere's the Redis script.")
    redis_script.run_example()

    log.info("\n\n\nHere's the Neo4J script.")
    neo4j_script.run_example()

    log.info(
        "\n\n\nHere's the persistence/serialization (Pickle/Shelve) script.")
    simple_script.run_example(furniture)


if __name__ == '__main__':
    """
    orchestrate nosql examples
    """
    showoff_databases()
