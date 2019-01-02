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

        log.info('Step 3: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)

        log.info('Step 4: Print the plastic products')
        print('Plastic products')
        pprint.pprint(results)

        log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
        furniture.remove({"product_type": {"$eq": "Couch"}, "color": {"$eq": "Blue"}})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'product_type': 'Couch', 'color': 'Blue'}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        pprint.pprint(results)
        log.info('Modified to check that the Blue Recliner is still there')
        query = {'color': 'Blue'}
        results = furniture.find_one(query)
        print(f"Color: {results['color']} product type: {results['product_type']}")
        
        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        log.info('Parse modified data fields')
        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']} product type: {doc['product_type']} color: {doc['color']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Query Red items')
        redquery = {'color': 'Red'}
        redresults = furniture.find(redquery)
        for redr in redresults:
            print(f"Product: {redr['product_type']} color: {redr['color']} description: {redr['description']}")
        
        log.info('Step 9: Query couches') 
        couchquery = {'product_type': 'Couch'}
        couchresults = furniture.find(couchquery)
        for couchr in couchresults:
            print(f"Product: {couchr['product_type']} color: {couchr['color']} description: {couchr['description']}")
            
        log.info('Step 10: Delete the collection so we can start over')
        db.drop_collection('furniture')
