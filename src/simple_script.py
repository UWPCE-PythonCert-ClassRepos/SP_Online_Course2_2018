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

        shelf_file = shelve.open('data/shelve.dat')
        log.info("store data at key")
        shelf_file['key'] = furniture_items
        log.info("retrieve a COPY of data at key")
        read_items = shelf_file['key']

        assert read_items == furniture_items
        log.info("delete data stored at key")
        del shelf_file['key']
        shelf_file.close()

    def run_csv():
        """
        write and read a csv
        """

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
        data = [{'product': 'Red couch','description': 'Leather low back'},
        {'product': 'Blue couch','description': 'Cloth high back'},
        {'product': 'Coffee table','description': 'Plastic'},
        {'product': 'Red couch','description': 'Leather high back'}]
        s = json.dumps(data)
        pprint.pprint(s)
        j = json.loads(s)

        pprint.pprint(j)

    run_pickle()
    run_shelve()
    run_csv()
    run_json()

    return

