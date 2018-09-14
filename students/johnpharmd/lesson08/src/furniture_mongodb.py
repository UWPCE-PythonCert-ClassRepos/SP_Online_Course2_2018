import login_database
import pprint
import utilities

log = utilities.configure_logger('default', '../logs/furniture_mongodb.log')


def update_furniture():
    """
        Updates furniture db in mongodb, according to assignmt instructions
    """

    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        furniture = db['furniture']

        # cursor = furniture.find({})
        # log.info('Here are all the furniture products\n')
        # for doc in cursor:
        #     pprint.pprint(doc)
        #     print()

        log.info('\nNow will update all product documents ' +
                 'to have a color field\n')
        furniture.update_many({}, {'$set': {'color': ''}})
        # newcursor = furniture.find({})
        # for doc in newcursor:
        #     pprint.pprint(doc)
        #     print()

        log.info('\nNow will rename "product" to "product_type"\n')
        furniture.update_many({}, {'$rename': {'product': 'product_type'}})
        # for doc in furniture.find({}):
        #     pprint.pprint(doc)
        #     print()

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
        log.info('\nNow deleting any documents that have "product type" ' +
                 'field\n')
        furniture.delete_many({'product type': '$'})

        log.info('Finally, printing all documents in furniture collection:\n')
        for doc in furniture.find({}):
            # for color in ('blue', 'red'):
            # if color in doc['product_type']:
            # furniture.update({doc['product_type'].strip(color)},
            # {doc['color']: {'$set': {'color':
            # color}}})
            pprint.pprint(doc)
            print()


if __name__ == '__main__':
    update_furniture()
