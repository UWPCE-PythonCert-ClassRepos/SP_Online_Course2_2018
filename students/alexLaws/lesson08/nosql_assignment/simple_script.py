"""
pickle etc
"""

import pickle
import shelve
import csv
import json

import pprint
import utilities

log = utilities.configure_logger('default', 'logs/mongodb_script.log')


def run_example(furniture_items):
    """
    various persistence and serialization scenarios

    """

    '''
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
    '''

    def alex_csv():
        """
        read and write an example CSV for testing purposes
        """

        fantasy_novels = [
            ('A Game of Thrones', 1, 694, 1996, 'George RR Martin', 'A Song of Ice and Fire'),
            ('A Clash of Kings', 2, 768, 1999, 'George RR Martin', 'A Song of Ice and Fire'),
            ('A Storm of Swords', 3, 973, 2000, 'George RR Martin', 'A Song of Ice and Fire'),
            ('A Feast for Crows', 4, 753, 2005, 'George RR Martin', 'A Song of Ice and Fire'),
            ('A Dance With Dragons', 5, 1040, 2011, 'George RR Martin', 'A Song of Ice and Fire'),
            ('The Name of The Wind', 1, 662, 2007, 'Patrick Rothfuss', 'The Kingkiller Chronicles'),
            ('The Wise Man\'s Fear', 2, 994, 2011, 'Patrick Rothfuss', 'The Kingkiller Chronicles'),
            ('The Way of Kings', 1, 1001, 2010, 'Brandon Sanderson', 'The Stormlight Archive'),
            ('Words of Radiance', 2, 1087, 2014, 'Brandon Sanderson', 'The Stormlight Archive'),
            ('Oathbringer', 3, 1248, 2017, 'Brandon Sanderson', 'The Stormlight Archive')
            ]
        log.info("Write a csv file of fantasy novels")
        with open('fantasy_novels.csv', 'w') as novels:
            novelwriter = csv.writer(novels)
            novelwriter.writerow(fantasy_novels)

        log.info("Print the file back")
        with open('fantasy_novels.csv', 'r') as books:
            book_info = csv.reader(books, delimiter=',', quotechar='"')
            for row in book_info:
                pprint.pprint(row)

    alex_csv()

    return
