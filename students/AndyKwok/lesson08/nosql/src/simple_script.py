"""
pickle etc
"""

import pickle
import shelve
import csv
import json

import pprint
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')


def run_example(furniture_items):
    """
    various persistence and serialization scenarios

    """

    def run_pickle():
        """
        Write and read with pickle
        """
        log.info("\n\n====")
        log.info('Step 1: Demonstrate persistence with pickle')
        log.info('Write a pickle file with the furniture data')

        pickle.dump(furniture_items, open('../data/data.pkl', 'wb'))

        log.info('Step 2: Now read it back from the pickle file')
        read_data = pickle.load(open('../data/data.pkl', 'rb'))
        log.info('Step 3: Show that the write and read were successful')
        assert read_data == furniture_items
        log.info("and print the data")
        pprint.pprint(read_data)

    def run_shelve():
        """
        write and read with shelve

        """
        log.info("\n\n====")
        log.info("Step 4: Demonstrate working with shelve")
        shelf_file = shelve.open('../data/shelve.dat')
        log.info("Step 5: store data at key")
        shelf_file['key'] = furniture_items

        log.info("Step 6: Now retrieve a COPY of data at key")
        read_items = shelf_file['key']

        log.info("Check it worked")
        assert read_items == furniture_items

        log.info("And now print the copy")
        pprint.pprint(read_items)

        log.info("Step 7: delete data stored at key to cleanup and close")
        del shelf_file['key']
        shelf_file.close()

    def run_csv():
        """
        write and read a csv
        """
        log.info("\n\n====")
        peopledata = [
            ('John', 'second guitar', 117.45),
            ('Paul', 'bass', 22.01),
            ('George', 'lead guitar', 45.99),
            ('Ringo', 'drume', 77.0),
            ('Roger', 'vocals', 12.5),
            ('Keith', 'drums', 6.25),
            ('Pete', 'guitar', 0.1),
            ('John', 'bass', 89.71)
        ]
        log.info("Step 8: Write csv file")
        with open('../data/rockstars.csv', 'w') as people:
            peoplewriter = csv.writer(people)
            peoplewriter.writerow(peopledata)

        log.info("Step 9: Read csv file back")
        with open('../data/rockstars.csv', 'r') as people:
            people_reader = csv.reader(people, delimiter=',', quotechar='"')
            for row in people_reader:
                pprint.pprint(row)

    def run_json():
        log.info("\n\n====")
        log.info("Step 10: Look at working with json data")
        furniture = [{'product': 'Red couch','description': 'Leather low back'},
        {'product': 'Blue couch','description': 'Cloth high back'},
        {'product': 'Coffee table','description': 'Plastic'},
        {'product': 'Red couch','description': 'Leather high back'}]

        log.info("Step 11: Return json string from an object")
        furniture_string = json.dumps(furniture)

        log.info("Step 12: Print the json")
        pprint.pprint(furniture_string)

        log.info("Step 13: Returns an object from a json string representation")
        furniture_object = json.loads(furniture_string)
        log.info("Step 14: print the string")
        pprint.pprint(furniture_object)

    run_pickle()
    run_shelve()
    run_csv()
    run_json()

    return


def run_nosql_ex():

    entries = [
        {
            'item': 'A',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10,
            'product_type': 'Couch',
            'ID': 999
        },
        {
            'product': 'B',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3,
            'product_type': 'Couch',
            'ID': 46
        },
        {
            'product': 'C',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25,
            'product_type': 'Table',
            'ID': 00
        },
        {
            'product': 'D',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17,
            'product_type': 'Couch',
            'ID': 66
        },
        {
            'product': 'E',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6,
            'product_type': 'Recliner',
            'ID': 75
        },
        {
            'product': 'F',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45,
            'product_type': 'Chair',
            'ID': 34
        },
        {
            'product': 'G',
            'description': 'Leather high back',
            'monthly_rental_cost': 20.99,
            'in_stock_quantity': 5,
            'product_type': 'Couch',
            'ID': 54
        },
        {
            'product': 'H',
            'description': 'Plastic',
            'monthly_rental_cost': 12.50,
            'in_stock_quantity': 4,
            'product_type': 'Desk',
            'ID': 4
        },
        {
            'product': 'I',
            'description': 'Plastic',
            'monthly_rental_cost': 56.8,
            'in_stock_quantity': 0,
            'product_type': 'Desk',
            'ID': 222
        },
        {
            'product': 'J',
            'description': 'Fiber',
            'monthly_rental_cost': 8,
            'in_stock_quantity': 9,
            'product_type': 'Desk',
            'ID': 1
        }
    ]
    
    def run_shelve():
        """
        write and read with shelve

        """
        log.info("\n====")
        shelf_file = shelve.open('../data/shelve.dat')
        log.info("Data are being saved into shelve database")
        shelf_file['key'] = entries
        log.info("Data saved")
        
        read_items = shelf_file['key']
        assert read_items == entries
        log.info("Data verified")
        
        log.info("\n====")
        log.info("Printing data from shelve database")
        pprint.pprint(read_items)

        del shelf_file['key']
        shelf_file.close()
    
    run_shelve()