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

        log.info('Step 3a: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        resultsa = furniture.find_one(query)

        log.info('Step 3b: Find the products that are described as Red')
        query = {'product_color': 'Red'}
        resultsb = furniture.find(query)
        for result in resultsb:
            print(f"\nproduct type: {result['product_type']}\n"
                  f"product color: {result['product_color']}\n"
                  f"description: {result['description']}\n"
                  f"rental cost: {result['monthly_rental_cost']}\n"
                  f"quantity in stock: {result['in_stock_quantity']}\n")


        log.info('Step 3c: Find the products that are described as Couch')
        query = {'product_type': 'Couch'}
        resultsc = furniture.find(query)
        for result in resultsc:
            print(f"\nproduct type: {result['product_type']}\n"
                  f"product color: {result['product_color']}\n"
                  f"description: {result['description']}\n"
                  f"rental cost: {result['monthly_rental_cost']}\n"
                  f"quantity in stock: {result['in_stock_quantity']}\n")

        log.info('Step 4a: Print the plastic products')
        print('Plastic products')
        pprint.pprint(resultsa)

        log.info('Step 4b: Print the Red products')
        print('Red products')
        pprint.pprint(resultsb)

        log.info('Step 4c: Print the Couch products')
        print('Couch products')
        pprint.pprint(resultsc)

        log.info('Step 5: Delete the Couch (actually deletes all couches)')
        furniture.remove({"product_type": {"$eq": "Couch"}})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'product_type': 'Couch'}
        results = furniture.find_one(query)
        print('The couches are now deleted, print should show none:')
        pprint.pprint(results)

        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']} product name: "
                  f"{doc['product_type']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')


def demonstrate_usage(car_data):
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        car = db['car']
        car.insert_many(car_data)

        log.info('Step 1: Find and print all trucks')
        query = {'car_type': 'Truck'}
        results = car.find(query)
        for result in results:
            print(f"\ncar type: {result['car_type']}\n"
                  f"car color: {result['car_color']}\n"
                  f"car year: {result['car_year']}\n"
                  f"car cost: {result['car_cost']}\n"
                  f"car location: {result['car_location']}\n")

        new_truck = {
                'car_type': 'Truck',
                'car_color': 'Purple',
                'car_year': '2019',
                'car_cost': 45000,
                'car_location': 'Florida'
            }

        car.insert(new_truck)

        log.info('Step 2: Find and print all trucks (including the newly '
                 'added truck')
        query = {'car_type': 'Truck'}
        results = car.find(query)
        for result in results:
            print(f"\ncar type: {result['car_type']}\n"
                  f"car color: {result['car_color']}\n"
                  f"car year: {result['car_year']}\n"
                  f"car cost: {result['car_cost']}\n"
                  f"car location: {result['car_location']}\n")
