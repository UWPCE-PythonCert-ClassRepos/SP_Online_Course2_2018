import pprint
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

def run_example(mailroom_entry):
    """
    mongodb data manipulation
    """

    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        mailroom_db = db['mailroom']

        mailroom_db.insert_many(mailroom_entry)

        # log.info('Step 3: Find the products that are described as plastic')
        # query = {'description': 'Plastic'}
        # results = mailroom_db.find_one(query)
        # log.info('Step 4: Print the plastic products')
        # print('Plastic products')
        # pprint.pprint(results)




        log.info(
            'Step 7: Find multiple documents, iterate though the results and print')

        cursor = furniture.find({'monthly_rental_cost': {'$gte': 15.00}}).sort('monthly_rental_cost', 1)
        print('Results of search')
        log.info('Notice how we parse out the data from the document')

        for doc in cursor:
            print(f"Cost: {doc['monthly_rental_cost']} product name: {doc['product']} Stock: {doc['in_stock_quantity']}")

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('furniture')

def mongodb_read_all():
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        mailroom_db = db['mailroom']
        mailroom_db.get_index()
        pprint.pprint(results)


    
def mongodb_del():
    log.info('Step 5: Delete the blue couch (actually deletes all blue couches)')
    furniture.remove({"product": {"$eq": "Blue couch"}})

def mongodb_read():
    log.info('Step 3: Find the products that are described as plastic')
    query = {'description': 'Plastic'}
    results = furniture.find_one(query)