"""
    mongodb example
"""

import pprint
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

sample_data = [
        {
            'manufacturer': 'Boeing',
            'product_type': 'airplane',
            'product_line': '787-9',
            'description': 'Long range aircraft',
            'range': 7635,
            'capacity': 280
        },
        {
            'manufacturer': 'Boeing',
            'product_type': 'airplane',
            'product_line': '787-8',
            'description': 'Long range aircraft',
            'range': 7355,
            'capacity': 242
        },
        {
            'manufacturer': 'Boeing',
            'product_type': 'airplane',
            'product_line': '787-10',
            'description': 'Long range aircraft',
            'range': 6430,
            'capacity': 310
        },
        {
            'manufacturer': 'Airbus',
            'product_type': 'airplane',
            'product_line': 'A350-900',
            'description': 'Long range aircraft',
            'range': 8100,
            'capacity': 325
        },
        {
            'manufacturer': 'Airbus',
            'product_type': 'airplane',
            'product_line': 'A350-900ULR',
            'description': 'Long range aircraft',
            'range': 9700,
            'capacity': 250
        },
        {
            'manufacturer': 'Airbus',
            'product_type': 'airplane',
            'product_line': 'A350-1000',
            'description': 'Long range aircraft',
            'range': 8000,
            'capacity': 366
        },
        {
            'manufacturer': 'Gulfstream',
            'product_type': 'airplane',
            'product_line': 'G650ER',
            'description': 'Business aircraft',
            'range': 7500,
            'capacity': 19
        },
        {
            'manufacturer': 'Gulfstream',
            'product_type': 'airplane',
            'product_line': 'G650',
            'description': 'Business aircraft',
            'range': 7000,
            'capacity': 19
        },
        {
            'manufacturer': 'Gulfstream',
            'product_type': 'airplane',
            'product_line': 'G600',
            'description': 'Business aircraft',
            'range': 6200,
            'capacity': 19
        },
        {
            'manufacturer': 'Lockheed Martin',
            'product_type': 'airplane',
            'product_line': 'SR-71',
            'description': 'Military aircraft',
            'range': 2900,
            'capacity': 3
        }

    ]

def run_example(airplane_data):
    """
    mongodb data manipulation
    """
    
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        fleet = db['fleet']

        log.info('What would you do if you won the lottery....')
        log.info('probably buy some airplanes')
        fleet.insert_many(airplane_data)

        log.info('now lets see our fleet')
        results = fleet.find()
        for i in results:
            print(i)

if __name__ == '__main__':
    run_example(sample_data)