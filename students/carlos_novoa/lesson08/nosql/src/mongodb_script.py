"""
    mongodb example
"""

import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    Refactored Mongo example
    """

    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        furniture = db['furniture']
        furniture.insert_many(furniture_items)

        # Just Red
        print('\n\n')
        log.info('Find only red products')
        query = {'color': {'$eq': 'Red'}}
        cursor = furniture.find(query)
        for doc in cursor:
            s = ('Product Type: {}, '
                 'Description: {},  '
                 'Color: {}, '
                 'Cost: {}, '
                 'Stock: {}')

            print(s.format(doc['product_type'],
                           doc['description'],
                           doc['color'],
                           doc['monthly_rental_cost'],
                           doc['in_stock_quantity']))
        print('\n\n')

        # Just couches
        log.info('Find only couches')
        query = {'product_type': {'$eq': 'couch'}}
        cursor = furniture.find(query)
        for doc in cursor:
            s = ('Product Type: {}, '
                 'Description: {},  '
                 'Color: {}, '
                 'Cost: {}, '
                 'Stock: {}')

            print(s.format(doc['product_type'],
                           doc['description'],
                           doc['color'],
                           doc['monthly_rental_cost'],
                           doc['in_stock_quantity']))
        print('\n\n')
        db.drop_collection('furniture')
