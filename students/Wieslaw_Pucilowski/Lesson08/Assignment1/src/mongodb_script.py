"""
    mongodb example
"""

import pprint
pp = pprint.PrettyPrinter(width=120)
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
            print(f"Cost: {doc['monthly_rental_cost']} product name: {doc['product']} Stock: {doc['in_stock_quantity']}")

        ##############################################################################################
        # Task 1
        # Add some extra furniture items 
        # separate the product field in to 2 fields; one called product type, one called color
        ##############################################################################################
        log.info('Step 8: Adding some new items with product field separated into 2 color and type')
        results = furniture.insert_many([
            {
                'product': {'type': 'leasure', 'color':'black'},
                'description': 'relaxing chair',
                'monthly_rental_cost': 22.99,
                'in_stock_quantity': 12
            },
            {
                'product': {'type': 'usless staff', 'color':'silver'},
                'description': 'iron curtains',
                'monthly_rental_cost': 8.99,
                'in_stock_quantity': 4
            },
            {
                'product': {'type': 'desk', 'color':'white'},
                'description': 'wooden kid desk',
                'monthly_rental_cost': 30.50,
                'in_stock_quantity': 19
            },
            {
                'product': {'type': 'couch', 'color':'Red'},
                'description': 'Leather front',
                'monthly_rental_cost': 10.50,
                'in_stock_quantity': 18
            }
        ])

        ##############################################################################################
        # Task 2
        # change the Mongodb program to store and retrieve using these new values
        ##############################################################################################
        log.info('Step 9: Store and retrieve using these new values')
        cursor = furniture.find()

        cursor1 = furniture.find({'product' : {'$type': 2}})

        cursor2 = furniture.find({ '$and':  [
                                    {'product' : {'$type': 3}},
                                    {'product.type' : { '$exists': 'true'}},
                                    {'product.color' : { '$exists': 'true'}}              
                                ]
                })
        for i in cursor1:
            print("""
    ******************************************************
    Product:        {}
    Description:    {}
    Monthly rental: {}
    Stock count:    {}
              """.format(i['product'],
                         i['description'],
                         i['monthly_rental_cost'],
                         i['in_stock_quantity'])
                )

        for i in cursor2:
            print("""
    ******************************************************
    Product type:   {}
    Product color:  {}
    Description:    {}
    Monthly rental: {}
    Stock count:    {}
              """.format(i['product']['type'],
                         i['product']['color'],
                         i['description'],
                         i['monthly_rental_cost'],
                         i['in_stock_quantity'])
                )

        ##############################################################################################
        # Task 3
        # Query to retrieve and print just the red products, an the just the couches
        ##############################################################################################
        log.info('Step 10: Search for items with color: red, type: couch')
        try:
            cursor = furniture.find({'$or': [
                { '$and': [
                    { 'product.type' : { '$exists': 'true', '$in': [ 'couch', 'Couch' ] } },
                    { 'product.color' : { '$exists': 'true', '$in': [ 'Red', 'red' ] } }
                ]},
                
                    {'$and': [
                        {'product' : {'$type': 2}}, 
                        {'product' : {'$regex': 'red', '$options': 'i'}},
                        {'product' : {'$regex': 'couch', '$options': 'i'}}
                        ]
                    }
                ]
            })
        except TypeError as e:
            print(e)
        for i in cursor:
            pp.pprint(i)

        cursor1 = furniture.find({'$and': [
                            {'product' : {'$type': 2}}, 
                            {'product' : {'$regex': 'red', '$options': 'i'}},
                            {'product' : {'$regex': 'couch', '$options': 'i'}}
                        ]
                    }
        )
        
        cursor2 = furniture.find({ '$and': [
                            { 'product.type' : { '$exists': 'true', '$in': [ 'couch', 'Couch' ] } },
                            { 'product.color' : { '$exists': 'true', '$in': [ 'Red', 'red' ] } }
                        ]}
        )

        for i in cursor1:
            print("""
    ******************************************************
    Product:        {}
    Description:    {}
    Monthly rental: {}
    Stock count:    {}
              """.format(i['product'],
                         i['description'],
                         i['monthly_rental_cost'],
                         i['in_stock_quantity'])
                )

        for i in cursor2:
            print("""
    ******************************************************
    Product type:   {}
    Product color:  {}
    Description:    {}
    Monthly rental: {}
    Stock count:    {}
              """.format(i['product']['type'],
                         i['product']['color'],
                         i['description'],
                         i['monthly_rental_cost'],
                         i['in_stock_quantity'])
                )

        log.info('Step 11: Delete the collection so we can start over')
        db.drop_collection('furniture')
