"""
pickle etc
"""

import pickle
import shelve
import csv
import json

import pprint
import src.utilities

log = src.utilities.configure_logger('default', 'logs/mongodb_script.log')


def run_example(furniture_items):
    """
    various persistence and serialization scenarios

    """

    def run_pickle():
        """
        Write and read with pickle
        """
        log.info("\n\n====")
        log.info('Demonstrate persistence with pickle')
        log.info('Write a pickle file with the furniture data')

        pickle.dump(furniture_items, open('data/data.pkl', 'wb'))

        log.info('Now read it back from the pickle file')
        read_data = pickle.load(open('data/data.pkl', 'rb'))
        log.info('Show that the write and read were successful')
        assert read_data == furniture_items
        log.info("and print the data")
        pprint.pprint(read_data)

    def run_shelve():
        """
        write and read with shelve

        """
        log.info("\n\n====")
        log.info("Demonstrate working with shelve")
        shelf_file = shelve.open('data/shelve.dat')
        log.info("store data at key")
        shelf_file['key'] = furniture_items

        log.info("Now retrieve a COPY of data at key")
        read_items = shelf_file['key']

        log.info("Check it worked")
        assert read_items == furniture_items

        log.info("And now print the copy")
        pprint.pprint(read_items)

        log.info("delete data stored at key to cleanup and close")
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
        log.info("Write csv file")
        with open('data/rockstars.csv', 'w') as people:
            peoplewriter = csv.writer(people)
            peoplewriter.writerow(peopledata)

        log.info("Read csv file back")
        with open('data/rockstars.csv', 'r') as people:
            people_reader = csv.reader(people, delimiter=',', quotechar='"')
            for row in people_reader:
                pprint.pprint(row)

    def run_json():
        log.info("\n\n====")
        log.info("Look at working with json data")
        furniture = [{'product': 'Red couch','description': 'Leather low back'},
        {'product': 'Blue couch','description': 'Cloth high back'},
        {'product': 'Coffee table','description': 'Plastic'},
        {'product': 'Red couch','description': 'Leather high back'}]

        log.info("Return json string from an object")
        furniture_string = json.dumps(furniture)

        log.info("Print the json")
        pprint.pprint(furniture_string)

        log.info("Returns an object from a json string representation")
        furniture_object = json.loads(furniture_string)
        log.info("print the string")
        pprint.pprint(furniture_object)

    run_pickle()
    run_shelve()
    run_csv()
    run_json()

    return
