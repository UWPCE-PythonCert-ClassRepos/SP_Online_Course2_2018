"""

NoSQL homework assignment

"""

import mongodb_assignment
import redis_assignment
import neo4j_assignment
import persistence_assignment
import utilities


def database_updates():
    """
    Homework assignment for database tasks.
    """

    log = utilities.configure_logger('default', '../logs/nosql_assignment.log')

    log.info('Running mongodb assignment.')
    mongodb_assignment.add_furniture()
    log.info('Running redis assignment.')
    redis_assignment.add_customers()
    log.info('Running neo4j assignment.')
    neo4j_assignment.add_people()


def persistence():
    """
    Homework assignment for persistence.
    """
    log = utilities.configure_logger('default', '../logs/nosql_assignment.log')

    log.info('Running persistence assignment.')
    persistence_assignment.run_json()


if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    database_updates()
    persistence()

