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

def run_example():
#def run_example(furniture_items):
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
        customers = [{'id': 1, 'first_name': 'Ross', 'last_name': 'Martin', 'zip_code': 94920, 'color': 'Blue'},
                     {'id': 2, 'first_name': 'Rachel', 'last_name': 'Martin', 'zip_code': 94920, 'color': 'Yellow'},
                     {'id': 3, 'first_name': 'Wolf', 'last_name': 'Martin', 'zip_code': 94920, 'color': 'Green'},
                     {'id': 4, 'first_name': 'Tom', 'last_name': 'Strobel', 'zip_code': 94920, 'color': 'Purple'},
                     {'id': 5, 'first_name': 'Holly', 'last_name': 'Strobel', 'zip_code': 94920, 'color': 'White'},
                     {'id': 6, 'first_name': 'Steve', 'last_name': 'Martin', 'zip_code': 27360, 'color': 'Blue'},
                     {'id': 7, 'first_name': 'Terrie', 'last_name': 'Martin', 'zip_code': 27360, 'color': 'Blue'},
                     {'id': 8, 'first_name': 'Morgan', 'last_name': 'Strobel', 'zip_code': 34567, 'color': 'Black'},
                     {'id': 9, 'first_name': 'Ryan', 'last_name': 'Strobel', 'zip_code': 94920, 'color': 'Green'},
                     {'id': 10, 'first_name': 'Roy', 'last_name': 'Trammell', 'zip_code': 23432, 'color': 'Blue'},
                    ]

        log.info("Step 11: Return json string from an object")
        customer_string = json.dumps(customers)

        log.info("Step 12: Print the json")
        pprint.pprint(customer_string)

        log.info("Step 13: Returns an object from a json string representation")
        customer_object = json.loads(customer_string)
        log.info("Step 14: print the string")
        pprint.pprint(customer_object)

    #run_pickle()
    #run_shelve()
    #run_csv()
    run_json()

    return
