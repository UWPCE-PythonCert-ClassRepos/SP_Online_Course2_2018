"""
    mongodb example
"""

import pprint

""""
from login_database import login_mongodb_cloud
from login_database import get_credentials
"""
import login_database


def run_example(furniture_items):
    """

    """
    credentials = login_database.get_credentials('mongodb_cloud')

    with login_database.login_mongodb_cloud(credentials) as client:
        #        logger.info('We are going to use a database called dev')
        #        logger.info('If it doesnt exist mongodb creates it')
        db = client['dev']

#        logger.info('And in that database use a collection called furniture')
#        logger.info('If it doesnt exist mongodb creates it')

        furniture = db['furniture']

#        logger.info('Now we add data from the dictionary above')
        results = furniture.insert_many(furniture_items)

#        logger.info('Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)

#        logger.info('Print the plastic products')
        pprint.pprint(results)

#        logger.info('Delete the blue couch (atually deletes all blue couches)')
        furniture.remove({"product": {"$eq": "Blue couch"}})

#        logger.info('Check it is deleted with a query and print')
        query = {'product': 'Blue couch'}
        results = furniture.find_one(query)
        pprint.pprint(results)

#        logger.info(
#            'Find multiple documents, iterate though the results and print')
#        logger.info('TBD')

#        logger.info('More sophisticated query examples')
#        logger.info('TBD')

#        logger.info('Using richer doucment structures')
#        logger.info('TBD')

#        logger.info('Delete the collection so we can start over')
#        db.drop_collection('furniture')

        # needed?
        # client.close()
#    logger.info('This should fail - if not try with explicit close')
    query = {'description': 'Plastic'}
    results = furniture.find_one(query)
#    logger.info('Print the plastic products')
    pprint.pprint(results)
    client.close()
