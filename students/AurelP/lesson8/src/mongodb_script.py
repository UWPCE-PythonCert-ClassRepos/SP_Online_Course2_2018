"""
    mongodb example
"""

import pprint
import login_database
import utilities

#log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    mongodb data manipulation
    """
    log = utilities.configure_logger('default', '../logs/mongodb_script.log')

    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called dev')
        log.info('But if it doesnt exist mongodb creates it')
        db = client['dev']
        db = client.dev

        log.info('And in that database use a collection called furniture')
        log.info('If it doesnt exist mongodb creates it')

        furniture = db['furniture']

        log.info('Step 2: Now we add data from the dictionary above')
        furniture.insert_many(furniture_items)

        #description='wood'
        log.info('Step 3: Find the products that are described as wood')
        query = {'description': 'Wood'}
        results = furniture.find(query)

        log.info('Step 4: Print the wood products')
        print('\nwood products')
        for res in results:
            print(f" product type: {res['product type']}\
                     color: {res['color']}\
                    description:  {res['description']}\
                    monthly_rental_cost:  {res['monthly_rental_cost']}\
                    in_stock_quantity:  {res['in_stock_quantity']}" )\

#        pprint.pprint(results)

        #color='red'
        log.info('Step 5: Find the products that are red color')
        query = {'color': 'Red'}
        results = furniture.find(query)

        log.info('Step 6: Print the red products')
        print('\nred products')
        #pprint.pprint(results)
        for res in results:
            print(f" product type: {res['product type']}\
                     color: {res['color']}\
                    description:  {res['description']}\
                    monthly_rental_cost:  {res['monthly_rental_cost']}\
                    in_stock_quantity:  {res['in_stock_quantity']}" )\

        #'product type': 'Couch'
        log.info('Step 7: Find the couches')
        query = {'product type': 'Couch'}
        results = furniture.find(query)

        log.info('Step 8: Print the couches')
        print('\ncouches products')
        #pprint.pprint(results)
        for res in results:
            print(f" product type: {res['product type']}\
                     color: {res['color']}\
                    description:  {res['description']}\
                    monthly_rental_cost:  {res['monthly_rental_cost']}\
                    in_stock_quantity:  {res['in_stock_quantity']}" )\


        #black wood products
        log.info('Step 9: Find the couches')
        query = {"$and": [{'color': 'Black'},
                          {'description': 'Wood'}]}
        results = furniture.find(query)

        log.info('Step 10: Print the black wood products')
        print('\nblack wood products')
        #pprint.pprint(results)
        for res in results:
            print(f" product type: {res['product type']}\
                     color: {res['color']}\
                    description:  {res['description']}\
                    monthly_rental_cost:  {res['monthly_rental_cost']}\
                    in_stock_quantity:  {res['in_stock_quantity']}" )\


        # log.info('Step 11: Delete the blue couch (actually deletes all blue couches)')
        # furniture.remove({"product": {"$eq": "Blue couch"}})

        # log.info('Step 6: Check it is deleted with a query and print')
        # query = {'product': 'Blue couch'}
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
        #     print(f"Cost: {doc['monthly_rental_cost']} product name: {doc['product']} Stock: {doc['in_stock_quantity']}")
        #
        log.info('Step 99: Delete the collection so we can start over')
        db.drop_collection('furniture')
