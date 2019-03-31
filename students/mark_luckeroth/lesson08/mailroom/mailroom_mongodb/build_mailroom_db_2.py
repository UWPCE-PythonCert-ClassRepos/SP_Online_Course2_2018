"""
    Lesson 08 mailroom mongodb assignment
    build baseline database
"""

import logging
import login_database
import pprint
import initial_donor_data

def populate_donordata():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    log.info('Build Donor Database')


    with login_database.login_mongodb_cloud() as client:
        log.info('Step 1: We are going to use a database called mailroom')
        log.info('But if it doesnt exist mongodb creates it')
        db = client['mailroom']

        log.info('And in that database use a collection called donors')
        log.info('If it doesnt exist mongodb creates it')

        donors = db['donors']

        log.info('Step 8: Delete the collection so we can start over')
        db.drop_collection('donors')

        log.info('Step 2: Now we add data from the dictionary in initial_donor_data.py')
        donor_data = initial_donor_data.get_donor_data()
        donors.insert_many(donor_data)

        log.info('Step 3: Find donor data by name')
        query = {'name': 'Paul Hollywood'}
        results = donors.find_one(query)

        print('Data for Paul Hollywood')
        pprint.pprint(results)

        log.info(
            'Step 7: Find all')

        cursor = donors.find()
        print('Results of search')
        for doc in cursor:
            print(f"Name: {doc['name']} donation amounts: {doc['amount']}")

        log.info('Step 7: Add a donor')
        new_donor_data = {
                    'name': 'Mark Luckeroth',
                    'amount': []}
        donors.insert_one(new_donor_data)
        cursor = donors.find()
        print('Results of search')
        for doc in cursor:
            print(f"Name: {doc['name']} donation amounts: {doc['amount']}")

        log.info('Step 7: Add a donation')
        donors.update_one(
                          {'name': 'Mark Luckeroth'},
                          {'$push': {'amount': 999.}})
        donors.update_one(
                          {'name': 'Paul Hollywood'},
                          {'$push': {'amount': 99.}})
        cursor = donors.find()
        print('Results of search')
        for doc in cursor:
            print(f"Name: {doc['name']} donation amounts: {doc['amount']}")


        log.info('step 9: pull and ID and recall with ID')
        query = donors.find_one({'name': 'Paul Hollywood'})
        print(query['_id'])

        recall = donors.find_one({'_id': query['_id']})
        print(recall['name'], recall['amount'])





if __name__ == '__main__':
    populate_donordata()
