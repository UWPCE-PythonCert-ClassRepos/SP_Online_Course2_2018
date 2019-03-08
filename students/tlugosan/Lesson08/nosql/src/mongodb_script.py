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

        # log.info('Step 3: Find the products that are described as plastic')
        # query = {'description': 'Plastic'}
        # results = furniture.find_one(query)
        #
        # log.info('Step 4: Print the plastic products')
        # print('Plastic products')
        # pprint.pprint(results)

        log.info('Step 4.1: Find all the products that are only red')
        red_query = {'color': 'Red'}
        red_results = furniture.find(red_query)
        log.info('Step 4.2: Print all the objects that are red')
        print('Red objects')
        print(red_results.count())
        for obj in red_results:
            pprint.pprint(obj)

        print('--------------------------------------')
        log.info('Step 4.2: Find all the red couches')
        red_couches = furniture.find({'product_type': 'Couch', 'color': 'Red'})
        log.info('Step 4.2: Print all the  red couches')
        print('Couches')
        print(red_couches.count())
        for obj in red_couches:
            pprint.pprint(obj)

        print('----------------------------------')
        # log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
        # furniture.remove({"product_type": {"$eq": "Blue couch"}})
        #
        # log.info('Step 6: Check it is deleted with a query and print')
        # query = {'product_type': 'Blue couch'}
        # results = furniture.find_one(query)
        # print('The blue couch is deleted, print should show none:')
        # pprint.pprint(results)
        #
        # log.info(
        #     'Step 7: Find multiple documents, iterate though the results and print')
        #
        # cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        # print('Results of search')
        # log.info('Notice how we parse out the data from the document')
        #
        # for doc in cursor:
        #     print(f"Cost: {doc['monthly_rental_cost']} product name: "
        #           f"{doc['product_type']} Stock: {doc['in_stock_quantity']}")
        #
        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')
