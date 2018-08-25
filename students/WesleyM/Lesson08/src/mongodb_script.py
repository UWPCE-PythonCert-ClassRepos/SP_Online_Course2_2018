"""
    mongodb example
"""

import pprint
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    mongodb data manipulation
    """

    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called dev')
        log.info('But if it doesnt exist mongodb creates it')
        db = client['dev']

        log.info('And in that database use a collection called furniture')
        log.info('If it doesnt exist mongodb creates it')

        furniture = db['furniture']

        log.info('Step 2: Now we add data from the dictionary above')
        furniture.insert_many(furniture_items)

        log.info('Step 3: Retrieve all the red products')
        query = {'product_color': 'Red'}
        results = furniture.find(query)
        print('Red Products')
        for item in results:
            pprint.pprint(item)

        log.info('Step 4: Retrieve all the couches')
        query = {'product_type': 'Couch'}
        results = furniture.find(query)
        print('Couches')
        for item in results:
            pprint.pprint(item)

        log.info('Step 5: Delete the collection so we can start over')
        db.drop_collection('furniture')
