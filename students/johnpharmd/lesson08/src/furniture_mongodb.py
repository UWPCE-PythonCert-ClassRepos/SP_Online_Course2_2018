import login_database
import pprint
import utilities

log = utilities.configure_logger('default', '../logs/furniture_mongodb.log')


def update_furniture():
    """
        Updates furniture db in mongodb, according to assignment instructions
    """

    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        furniture = db['furniture']

        log.info('\nNow will update all product documents ' +
                 'to have a color field\n')
        furniture.update_many({}, {'$set': {'color': ''}})

        log.info('\nNow will rename "product" to "product_type"\n')
        furniture.update_many({}, {'$rename': {'product': 'product_type'}})

        log.info('\nNow will check each product type for colors "blue" ' +
                 'and "red". If either is found, will remove from product ' +
                 'type and add to color field\n')
        furniture.update_many({'product_type': 'Blue couch'},
                              {'$set': {'color': 'Blue'}})
        furniture.update_many({'product_type': 'Blue couch'},
                              {'$set': {'product_type': 'Couch'}})
        furniture.update_many({'product_type': 'Blue recliner'},
                              {'$set': {'color': 'Blue'}})
        furniture.update_many({'product_type': 'Blue recliner'},
                              {'$set': {'product_type': 'Recliner'}})
        furniture.update_many({'product_type': 'Red couch'},
                              {'$set': {'color': 'Red'}})
        furniture.update_many({'product_type': 'Red couch'},
                              {'$set': {'product_type': 'Couch'}})

        log.info('Adding two new furniture items:\n')
        new_furniture = [
            {
                'product_type': 'Lamp',
                'description': 'Ceramic',
                'monthly_rental_cost': 3.99,
                'in_stock_quantity': 4,
                'color': 'Red'
            },
            {
                'product': 'Couch',
                'description': 'Cloth low back',
                'monthly_rental_cost': 6.99,
                'in_stock_quantity': 3,
                'color': 'Blue'
            }
        ]
        furniture.insert_many(new_furniture)

        log.info('Printing all documents in furniture collection:\n')
        for doc in furniture.find({}):
            pprint.pprint(doc)
            print()

        log.info('Query for all red products')
        query = {'color': 'Red'}
        cursor = furniture.find(query)
        print('Printing all red products:\n')
        for doc in cursor:
            pprint.pprint(doc)
            print()

        log.info('\nQuery for all couches')
        query = {'product_type': 'Couch'}
        cursor = furniture.find(query)
        print('Printing all couches:\n')
        for doc in cursor:
            pprint.pprint(doc)
            print()


if __name__ == '__main__':
    update_furniture()
