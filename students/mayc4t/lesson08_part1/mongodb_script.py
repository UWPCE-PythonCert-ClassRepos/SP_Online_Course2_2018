"""Self-contained mongodb example."""

import configparser
from pathlib import Path
import pprint
import pymongo
import seed_data

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

def login_mongodb_cloud():
    """Connect to mongodb and login."""

    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]
        print(f'Got user=***** pw=***** from {config_file}')
    except Exception as e:
        print(f'Error parsing {config_file}: {e}')

    client = pymongo.MongoClient(f'mongodb+srv://{user}:{pw}'
                                 '@cluster0-np6jb.gcp.mongodb.net/test'
                                 '?retryWrites=true')

    return client


def run_mongodb_example():
    """Mongodb example from course, extended as needed for lesson08."""

    furniture_items = seed_data.get_furniture_data()

    with login_mongodb_cloud() as client:
        # First, get a handle to the database called dev. If dev doesn't exist,
        # then it's created.
        print('\nStep 1: Connect to "dev" DB (created if needed)'
              '; use furniture collection (created if needed).')
        db = client['dev']
        furniture = db['furniture']

        print('\nStep 2: Insert furniture_items dict into furniture DB.')
        furniture.insert_many(furniture_items)

        print('\nStep 3: Find the products that are described as plastic.')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)

        print('\nStep 4: Print the plastic products.')
        print('Plastic products')
        pprint.pprint(results)

        print('\nStep 5: Delete all blue couches.')
        furniture.remove({"product": {"$eq": "Couch"},
                          "color": {"$eq": "Blue"}})

        print('\nStep 6: Show no blue couches with a query and print.')
        query = {'product': 'Couch',
                 'color': 'Blue'}
        results = furniture.find_one(query)
        print('blue couch query returned:')
        pprint.pprint(results)

        print('\nStep 7: Find and iterate over multiple documents.')
        cursor = (furniture.find({'monthly_rental_cost': {'$gte': 15.00}})
                  .sort('monthly_rental_cost', 1))
        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']}"
                  f" product name: {doc['product']}"
                  f" Stock: {doc['in_stock_quantity']}")

        print('\nStep 8: Get all red products.')
        query = {'color': 'Red'}
        red_products = furniture.find(query)
        for doc in red_products:
            seed_data.print_furniture_item(doc)

        print('\nStep 9: Get all couches (note, blue couches deleted above).')
        query = {'product': 'Couch'}
        couches = furniture.find(query)
        for doc in couches:
            seed_data.print_furniture_item(doc)

        print('\nFinally: Delete furniture collection so we can start over.')
        db.drop_collection('furniture')

if __name__ == '__main__':
    run_mongodb_example()
