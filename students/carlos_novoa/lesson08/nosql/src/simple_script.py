"""
    Persistence and serialization
"""

import pickle
import pprint
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    Refactored Pickle example
    """

    items = [
        {
            'name': 'Jim',
            'department': 'sales',
            'salary': '45,000',
            'company': 'Dunder Mifflin',
            'hair': 'Brown'
        },
        {
            'name': 'Pam',
            'department': 'sales',
            'salary': '35,000',
            'company': 'Dunder Mifflin',
            'hair': 'Brown'
        },
        {
            'name': 'Dwight',
            'department': 'sales',
            'salary': '44,000',
            'company': 'Dunder Mifflin',
            'hair': 'Brown'
        },
        {
            'name': 'Michael',
            'department': 'sales',
            'salary': '50,000',
            'company': 'Dunder Mifflin',
            'hair': 'Dark Brown'
        },
        {
            'name': 'Ryan',
            'department': 'sales',
            'salary': '33,000',
            'company': 'Dunder Mifflin',
            'hair': 'Black'
        },
        {
            'name': 'Andy',
            'department': 'sales',
            'salary': '55,000',
            'company': 'Dunder Mifflin',
            'hair': 'Brown'
        },
        {
            'name': 'Creed',
            'department': 'sales',
            'salary': '23,000',
            'company': 'Dunder Mifflin',
            'hair': 'Gray'
        },
        {
            'name': 'Phyllis',
            'department': 'sales',
            'salary': '39,000',
            'company': 'Dunder Mifflin',
            'hair': 'Brown'
        },
        {
            'name': 'Oscar',
            'department': 'sales',
            'salary': '42,000',
            'company': 'Dunder Mifflin',
            'hair': 'Black'
        },
        {
            'name': 'Kevin',
            'department': 'accounting',
            'salary': '37,000',
            'company': 'Dunder Mifflin',
            'hair': 'Brown'
        }
    ]

    def run_pickle():
        pickle.dump(items, open('../data/ndata.pkl', 'wb'))
        read_data = pickle.load(open('../data/ndata.pkl', 'rb'))
        pprint.pprint(read_data)

    run_pickle()
    return
