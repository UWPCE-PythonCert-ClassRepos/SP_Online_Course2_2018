"""

Integrated example for nosql databases

"""

import learn_data
import mongodb_script
import redis_script
import neo4j_script
import persistence_serialization
import simple_script
import utilities


def showoff_databases():
    """
    Here we illustrate basic interaction with nosql databases
    """

    log = utilities.configure_logger('default', '../logs/nosql_dev.log')

    log.info("Mongodb example to use data from Furniture module, so get it")
    furniture = learn_data.get_furniture_data()

    roygbiv = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"]
    
    for item in furniture:
        product_type = item['product']
        color_name = 'N/A'
        for color in roygbiv:
            if color in product_type:
                color_name = color
                product_type = product_type.replace(color, '').lstrip(' ')
                break

        item['color'] = color_name
        item['product type'] = product_type

    mongodb_script.run_example(furniture)

    log.info("Other databases use data embedded in the modules")

    redis_script.run_example()
    neo4j_script.run_example()
    simple_script.run_example(furniture)
    persistence_serialization.run_json()


if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    showoff_databases()
