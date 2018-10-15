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
    input('Simple Script. Press Enter to continue........')
    
    def run_pickle(data):
        """
        Write and read with pickle
        """
        input('Pickle Example.............')
        log.info("\n\n====")
        log.info('Step 1: Demonstrate persistence with pickle')
        log.info('Write a pickle file with the furniture data')

        pickle.dump(data, open('../data/data.pkl', 'wb'))
        
        log.info('Step 2: Now read it back from the pickle file')
        read_data = pickle.load(open('../data/data.pkl', 'rb'))

        log.info('Step 3: Show that the write and read were successful')
        assert read_data == furniture_items
        log.info("and print the data")
        pprint.pprint(read_data)

    def run_shelve(data):
        """
        Write and read with shelve
        """
        input('Shelve Example..............')
        log.info("\n\n====")
        log.info("Step 4: Demonstrate working with shelve")
        shelf_file = shelve.open('../data/shelve.dat')

        log.info("Step 5: store data at key")
        shelf_file['key'] = data

        log.info("Step 6: Now retrieve a COPY of data at key")
        read_items = shelf_file['key']
        log.info("Check it worked")
        assert read_items == data
        log.info("And now print the copy")
        pprint.pprint(read_items)

        log.info("Step 7: delete data stored at key to cleanup and close")
        del shelf_file['key']
        shelf_file.close()

    def run_csv():
        """
        write and read a csv
        """
        input('CSV Example..............')
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

    def run_json(data):
        input('JSON Example..............')
        log.info("\n\n====")
        log.info("Step 11: Return json string from an object (json.dumps)")
        data_string = json.dumps(data)

        log.info("Step 12: Print the json")
        pprint.pprint(data_string)

        log.info("Step 13: Returns an object from a json string representation")
        data_object = json.loads(data_string)

        log.info("Step 14: print the string")
        pprint.pprint(data_object)

    def json_to_pickle(json_data):
        input('JSON to Pickle convert.........')
        with open(json_data, 'r') as json_file:
            data = json.load(json_file)
            pickle.dump(data, open('../data/json_data.pkl', 'wb'))
            yea = pickle.load(open('../data/json_data.pkl', 'rb'))
            pprint.pprint(yea)
            assert yea == data
        
    
    log.info('Assignment: Pick one of the 4 formats only.')
    log.info('Create some data (at least 10 rows with about 5 fields in each).')
    log.info('Show how you can read and write data in that format.')   
    run_pickle(furniture_items)
    run_shelve(furniture_items)
    run_csv()
    run_json(furniture_items)

    log.info('For an extra assignment, write a program that reads one format and converts to another.')
    with open('../data/furniture.json', 'w+') as json_file:
        json.dump(furniture_items, json_file)
    json_to_pickle('../data/furniture.json')

    
    
    return
