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
        log.info('Using Dev database...')
        db = client['dev']

        log.info('Using Furniture collection...')

        furniture = db['furniture']

        log.info('Adding data from the dictionary above...')
        furniture.insert_many(furniture_items)

        log.info('Query 1: Find all red products')
        query = {'color': 'Red'}
        results = furniture.find(query)

        print('\nRed products: \n')
        for row in results:
            print(f"Product: {row['product']}\n" +
                  f"Color: {row['color']}\n" +
                  f"Description: {row['description']}\n" +
                  f"Cost: {row['monthly_rental_cost']}\n" +
                  f"Stock: {row['in_stock_quantity']}\n")

        log.info('Query 2: Find all couches')
        query = {'product': 'Couch'}
        results = furniture.find(query)

        print('\nAll couches: \n')
        for row in results:
            print(f"Product: {row['product']}\n" +
                  f"Color: {row['color']}\n" +
                  f"Description: {row['description']}\n" +
                  f"Cost: {row['monthly_rental_cost']}\n" +
                  f"Stock: {row['in_stock_quantity']}\n")

        log.info('Finally: Delete the collection so we can start over')
        db.drop_collection('furniture')
