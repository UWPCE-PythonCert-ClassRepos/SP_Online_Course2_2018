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
        
        log.info('** Add new item')
        new_item = {
            'product':
                {'type': 'Stool',
                 'color': 'White'},
            'description': 'Wood',
            'monthly_rental_cost': 18.99,
            'in_stock_quantity': 8
        }
        furniture.insert_one(new_item)

        log.info('Step 2: Now we add data from the dictionary above')
        furniture.insert_many(furniture_items)

        log.info('Step 3: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)
        
        log.info('** Find all products that are red')
        query_red = {'product.color': 'Red'}
        results_red = furniture.find(query_red)

        log.info('Step 4: Print the plastic products')
        print('Plastic products')
        pprint.pprint(results)
        
        log.info('** Print the red products')
        print('Red products')
        for item in results_red:
            pprint.pprint(item)

        log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
        furniture.remove({'$and': [{'product.type': 'Couch'},
                                  {'product.color': 'Blue'}]})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'$and': [{'product.type': 'Couch'},
                          {'product.color': 'Blue'}]}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        pprint.pprint(results)

        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']} product name: {doc['product']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')
