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

        log.info('Step 3: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)

        log.info('Step 4: Print the plastic products')
        print('Plastic products')
        pprint.pprint(results)

        log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
        furniture.remove({"product": {"$eq": "Blue couch"}})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'product': 'Blue couch'}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        pprint.pprint(results)

        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        for doc in cursor:
            print(
                f"Cost: {doc['monthly_rental_cost']} product name: {doc['product']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')

def run_exercise(furniture_items):
    """
    mongodb exercise

    Assignment:
    Add some extra furniture items for mongodb.
    Separate the product field in to 2 fields; product type, and color.
    Start by amending the data, then change the Mongodb program to store
    and retrieve using these new values.

    Next, write a mongodb query to retrieve and print just the red products,
    and the just the couches.

    """

    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: Create database and furniture collection')
        db = client['dev']
        db.drop_collection('furniture')
        furniture = db['furniture']

        log.info('Step 2: Add data from the dictionary')
        furniture.insert_many(furniture_items)

        log.info('Step 3: Find the products that are described as plastic')
        query = {'description': 'Plastic'}
        results = furniture.find_one(query)

        log.info('Step 4: Print the plastic products')
        print('Plastic products')
        pprint.pprint(results)

        # STEP 5 modified for assignment
        log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
        furniture.remove({"$and": [{"product": {"$eq": "Couch"}},
                                   {"color": {"$eq": "Blue"}}]})

        # STEP 6 modified for assigment
        log.info('Step 6: Check it is deleted with a query and print')
        query = {"$and": [{"product": {"$eq": "Couch"}},
                                   {"color": {"$eq": "Blue"}}]}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        pprint.pprint(results)

        # STEP 6A added for assignment
        log.info('Step 6a: Check that other colored couches still exist')
        query = {'product': 'Couch'}
        results = furniture.find_one(query)
        print('Print should show an existing couch:')
        pprint.pprint(results)

        # STEP 7 modified for assignment
        log.info('Step 7: Find multiple documents, iterate though the results and print')
        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')
        for doc in cursor:
            print(f"Cost: ${doc['monthly_rental_cost']:.2f}, Product: {doc['product']}, "
                  f"Color: {doc['color']}, Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')
