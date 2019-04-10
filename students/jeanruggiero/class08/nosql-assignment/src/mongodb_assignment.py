"""
    mongodb homework assignment
"""

import pprint
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_assignment.log')


def add_furniture():
    """
    mongodb assignment - add furniture items, separate the product field into
    two fields: product type and color. Write a mongodb query to retrieve and
    print just the red products, then just the couches.
    """

    furniture_data = [
        {
            'product type': 'couch',
            'color': 'red',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product type': 'couch',
            'color': 'blue',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product type': 'Coffee table',
            'color': 'brown',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product type': 'couch',
            'color': 'red',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product type': 'recliner',
            'color': 'blue',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product type': 'Chair',
            'color': 'red',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        },
        {
            'product type': 'barstool',
            'color': 'orange',
            'description': 'metal',
            'monthly_rental_cost': 3.00,
            'in_stock_quantity': 23
        },
        {
            'product type': 'desk',
            'color': 'purple',
            'description': 'wood',
            'monthly_rental_cost': 200.00,
            'in_stock_quantity': 1
        },
        {
            'product type': 'bed',
            'color': 'white',
            'description': 'wood',
            'monthly_rental_cost': 89.99,
            'in_stock_quantity': 5
        }
    ]

    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called dev')
        log.info('But if it doesnt exist mongodb creates it')
        db = client['dev']

        log.info('And in that database use a collection called furniture')
        log.info('If it doesnt exist mongodb creates it')
        furniture = db['furniture']

        log.info('Step 2: Now we add data from the dictionary above')
        furniture.insert_many(furniture_data)

        log.info('Step 3: Find the products that are red.')
        query = {'color': 'red'}
        results = furniture.find(query)

        log.info('Step 4: Print the red products')
        print('Red products')
        for result in results:
            pprint.pprint(result)

        log.info('Step 5: Find the couches.')
        query = {'product type': 'couch'}
        results = furniture.find(query)

        log.info('Step 6: Print the couches.')
        print('Couches')
        for result in results:
            pprint.pprint(result)

        log.info('Step 7: Delete the collection so we can start over')
        db.drop_collection('furniture')
