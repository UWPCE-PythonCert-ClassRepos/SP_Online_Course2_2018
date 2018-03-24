"""
    mongodb example
"""

import pprint
import src.login_database
import src.utilities

log = src.utilities.configure_logger('default', 'logs/mongodb_script.log')

def run_example(furniture_items):
    """
    mongodb data manipulation
    """

    with src.login_database.login_mongodb_cloud() as client:
        log.info('We are going to use a database called dev')
        log.info('If it doesnt exist mongodb creates it')
        db = client['dev']

        log.info('And in that database use a collection called furniture')
        log.info('If it doesnt exist mongodb creates it')

        furniture = db['furniture']

        log.info('Now we add data from the dictionary above')
        furniture.insert_many(furniture_items)

        log.info('Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)

        log.info('Print the plastic products')
        pprint.pprint(results)

        log.info('Delete the blue couch (actually deletes all blue couches)')
        furniture.remove({"product": {"$eq": "Blue couch"}})

        log.info('Check it is deleted with a query and print')
        query = {'product': 'Blue couch'}
        results = furniture.find_one(query)
        pprint.pprint(results)

        log.info(
            'Find multiple documents, iterate though the results and print')
        log.info('TBD')

        log.info('More sophisticated query examples')
        log.info('TBD')

        log.info('Using richer document structures')
        log.info('TBD')

        log.info('Delete the collection so we can start over')
        db.drop_collection('furniture')

