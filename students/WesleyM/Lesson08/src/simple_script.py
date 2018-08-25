"""
pickle etc
"""

import pickle
import shelve
import csv
import json

import pprint
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    various persistence and serialization scenarios

    """


    def run_json():
        log.info("\n\n====")
        log.info("Step 1: Look at working with json data")
        furniture = [
            {
            'product type': 'Couch',
            'product color': 'Red',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product type': 'Couch',
            'product color': 'Blue',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product type': 'Coffee table',
            'product color': 'Black',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product_type': 'Couch',
            'product_color': 'Red',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product_type': 'Recliner',
            'product_color': 'Blue',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product_type': 'Chair',
            'product_color': 'White',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        },
        {
            'product_type': 'Standing desk',
            'product_color': 'White',
            'description': 'Plastic',
            'monthly_rental_cost': 100.00,
            'in_stock_quantity': 10
        },
        {
            'product_type': 'Futon',
            'product_color': 'Beige',
            'description': 'Foam',
            'monthly_rental_cost': 200.00,
            'in_stock_quantity': 2
        },
        {
            'product_type': 'Futon',
            'product_color': 'Red',
            'description': 'Foam',
            'monthly_rental_cost': 200.00,
            'in_stock_quantity': 2
        },
        {
            'product_type': 'Desk',
            'product_color': 'Rainbow',
            'description': 'Abomination',
            'monthly_rental_cost': 1000.00,
            'in_stock_quantity': 1
        }
        ]

        log.info("Step 2: Return json string from an object")
        furniture_string = json.dumps(furniture)

        log.info("Step 3: Print the json")
        pprint.pprint(furniture_string)

        log.info("Step 4: Returns an object from a json string representation")
        furniture_object = json.loads(furniture_string)
        log.info("Step 5: print the string")
        pprint.pprint(furniture_object)

    run_json()

    return
