"""
Shin Tran
Python 220
Lesson 8 Assignment
Mongodb example
"""

import pprint
import login_database
import utilities
import learn_data


log = utilities.configure_logger('default', '../logs/mongodb_script.log')
additional_furniture = [
    {
        'product': 'Chair',
        'product_color': 'Green',
        'description': 'Plastic back',
        'monthly_rental_cost': 8.99,
        'in_stock_quantity': 15
    },
    {
        'product': 'Chair',
        'product_color': 'Yellow',
        'description': 'Cushion back',
        'monthly_rental_cost': 14.99,
        'in_stock_quantity': 15
    }
]
blue_couch = {
    'product': 'Couch',
    'product_color': 'Blue',
    'description': 'Cloth high back',
    'monthly_rental_cost': 9.99,
    'in_stock_quantity': 3
}



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
        furniture.delete_many({"product": {"$eq": "Couch"}, "product_color": {"$eq": "Blue"}})

        log.info('Step 6: Check it is deleted with a query and print')
        query = {'product': 'Couch', 'product_color': 'Blue'}
        results = furniture.find_one(query)
        print('The blue couch is deleted, print should show none:')
        pprint.pprint(results)

        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']} product name: {doc['product']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Add two more furnitures to the database')
        furniture.insert_many(additional_furniture)
        query_new = {'in_stock_quantity': 15}
        results_new = furniture.find(query_new)
        print('Two additional furnitures have been added:')
        for new_item in results_new:
            pprint.pprint(new_item)

        log.info('Step 9: Print just the red products')
        query_red = furniture.find({'product_color': 'Red'})
        for red in query_red:
            pprint.pprint(red)

        log.info('Step 10: Print just the couch products')
        log.info('Adding the blue couch that was removed in step 5 back into the db')
        furniture.insert_one(blue_couch)
        query_couch = furniture.find({'product': 'Couch'})
        for couch in query_couch:
            pprint.pprint(couch)

        log.info('Step 11: Delete the collection so we can start over')
        db.drop_collection('furniture')


if __name__ == '__main__':
    furniture = learn_data.get_furniture_data()
    run_example(furniture)
