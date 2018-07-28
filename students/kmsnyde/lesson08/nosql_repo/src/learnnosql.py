"""

Integrated example for nosql databases

"""

import learn_data
import mongodb_script
import redis_script
import neo4j_script
import simple_script
import utilities
import employee_data
import mongodb_employee_script


def showoff_databases():
    """
    Here we illustrate basic interaction with nosql databases
    """

    log = utilities.configure_logger('default', '../logs/nosql_dev.log')

    log.info("Mongodb example to use data from Furniture module, so get it")
    furniture = learn_data.get_furniture_data()
    mongodb_script.run_example(furniture)

    log.info("Other databases use data embedded in the modules")

    redis_script.run_example()
    neo4j_script.run_example()
    simple_script.run_example(furniture)
    
    log.info('Running mongodb_emplyee_script for assignment')
    employee = employee_data.get_employee_data()
    mongodb_employee_script.run_example(employee)


if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    showoff_databases()
