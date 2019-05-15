"""
    mongodb example
"""

import pprint
import login_database as login_database
import utilities as utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    Modified for Lesson 8 part 1. In the data, we changed the
    decription from product to product_type and color. Step 5 and 6
    are modified to search for 'product_type'. Added a query to
    search for just red items and just couches.
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

        log.info('Step 3: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)

        log.info('Step 4: Print the plastic products')
        print('Plastic products')
        pprint.pprint(results)

        log.info('Step Assignment: Print the red couches only.')
        query_new = furniture.find({"$and":[{'product_type':'couch'},{'color':'Red'}]})
        #query_new = furniture.find({'color':'Red'})
        print('The red couches are')
        for item in query_new:
            print(f"Cost: {item['monthly_rental_cost']}"
                  f" product name: {item['product_type']} "
                  f"Stock: {item['in_stock_quantity']} "
                  f"Color:{item['color']}")


        log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
        furniture.remove({"product_type": {"$eq": "Blue couch"}})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'product_type': 'Blue couch'}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        pprint.pprint(results)

        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']} product name: {doc['product_type']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')
