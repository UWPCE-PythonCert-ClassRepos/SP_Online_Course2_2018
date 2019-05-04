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


def run_json():
    log.info("Step 1: Define data")
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
        },
        {
            'product type': 'bench',
            'color': 'yellow',
            'description': 'wood',
            'monthly_rental_cost': 56,
            'in_stock_quantity': 2
        }
    ]

    log.info("Step 2: Return json string from an object")
    furniture_string = json.dumps(furniture_data)

    log.info("Step 3: Print the json")
    pprint.pprint(furniture_string)

    log.info("Step 4: Write json to a file.")
    with open('furniture.json', 'w') as f:
        f.write(furniture_string)

    log.info("Step 5: Read json from file.")
    with open('furniture.json','r') as f:
        furniture_string = f.read()

    log.info("Step 6: Display object from json string representation in file")
    furniture_object = json.loads(furniture_string)
    pprint.pprint(furniture_object)
