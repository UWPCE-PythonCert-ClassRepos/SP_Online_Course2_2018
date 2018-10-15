"""
mongodb example
"""
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
        log.info('Delete all data')
        furniture.delete_many({"product": {"$ne": ""}})

        log.info('Step 2: Now we add data from the dictionary above')
        furniture.insert_many(furniture_items)

        log.info('Step 3: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find(query)

        log.info('Step 4: Print the plastic products')
        print('Plastic products (should be 2)')
        print_items(results)

        log.info(
            'Step 5: Delete the blue couch (actually deletes all blue couches)'
        )
        furniture.delete_many({'product_type': 'Couch', 'color': 'Blue'})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'product_type': 'Couch', 'color': 'Blue'}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        print_items(results)

        log.info('Step 7: Find multiple documents, '
                 'iterate though the results and print')
        log.info('Notice how we parse out the data from the document')
        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}
                               ).sort('monthly_rental_cost', 1)
        print('Results of search')
        print_items(cursor)

        log.info('Step 8: Find just the red-color products')
        query = furniture.find({'color': {'$eq': 'Red'}})
        print('Results of search should contain 2 couches and 1 recliner')
        print_items(query)

        log.info('Step 9: Find just the couches')
        query = furniture.find({'product_type': {'$eq': 'Couch'}})
        print(
            'Results of search should contain 2 red couches and 1 black couch')
        print_items(query)

        log.info('Step 10: Delete the collection so we can start over')
        db.drop_collection('furniture')

def print_items(items):
    if items:
        print(f"NUMBER OF FURNITURE ITEMS FOUND: {items.count()}")
        for item in items:
            print(f"=== Furniture Item ===")
            print(f"\tCost:         {item['monthly_rental_cost']}")
            print(f"\tProduct name: {item['product_type']}")
            print(f"\tDescription:  {item['description']}")
            print(f"\tColor:        {item['color']}")
            print(f"\tStock:        {item['in_stock_quantity']}")
    else:
        print("NO FURNITURE ITEMS FOUND!")