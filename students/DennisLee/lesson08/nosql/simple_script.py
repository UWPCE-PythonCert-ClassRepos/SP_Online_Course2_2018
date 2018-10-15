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

airplanes = [  # Raw data to transform into dict list before saving
    ('OEM', 'Model', 'Category', 'Seats per row', 'Width', 'Height'),
    ('Bombardier', 'C Series', 'Single aisle', '5', '138', '146'),
    ('McDonnell-Douglas', 'MD80', 'Single aisle', '5', '131.6', '142'),
    ('Boeing', 'B737', 'Single aisle', '6', '148', '158'),
    ('Boeing', 'B767', 'Twin aisle', '7', '198', '213'),
    ('Boeing', 'B787', 'Twin aisle', '9', '227', '234'),
    ('Boeing', 'B777', 'Twin aisle', '10', '244', '244'),
    ('Boeing', 'B747', 'Double decker', '15', '256', '303'),
    ('Airbus', 'A320', 'Single aisle', '6', '155.5', '163'),
    ('Airbus', 'A330', 'Twin aisle', '8', '222', '222'),
    ('Airbus', 'A350', 'Twin aisle', '9', '235', '240'),
    ('Airbus', 'A380', 'Double decker', '18', '281', '331')
]

all_planes = []  # List of airplane dictionary info to save
for i in range(1, len(airplanes)):
    dict_plane = {}
    for j in range(len(airplanes[0])):
        dict_plane[airplanes[0][j]] = airplanes[i][j]
    all_planes.append(dict_plane)

def run_example(furniture_items):
    """
    various persistence and serialization scenarios
    """
    def run_pickle():
        """
        write and read with pickle
        """
        read_data = None  # Define here to establish scope
        log.info("\n\n====")
        log.info('Step 1: Demonstrate persistence with pickle')
        log.info('Write a pickle file with the furniture data')

        pickle.dump(furniture_items, open('../data/data.pkl', 'wb'))

        log.info('Step 2: Now read it back from the pickle file')
        with open('../data/data.pkl', 'rb') as pickle_file:
            read_data = pickle.load(pickle_file)
        log.info('Step 3: Show that the write and read were successful')
        assert read_data == furniture_items
        log.info("and print the data")
        pprint.pprint(read_data)

    def save_pickle_file(data_name, file_name):
        """
        write data `data_name` to pickle db named `file_name`
        """
        log.info("SAVE PICKLE: Here's the data to save to a pickle file")
        pprint.pprint(data_name)

        log.info('SAVE PICKLE: Write a pickle file with some dictionary data')
        with open(file_name, 'wb') as pickle_file:
            pickle.dump(data_name, pickle_file)

    def load_pickle_file(file_name):
        """
        Load a pickle database `file_name` and pretty-print its data
        """
        data_values = None  # Define here to establish scope
        log.info("LOAD PICKLE: Open the pickle file")
        with open(file_name, 'rb') as pickle_file:
            data_values = pickle.load(pickle_file)

        log.info("LOAD PICKLE: Print the loaded pickle data")
        pprint.pprint(data_values)

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

    def convert_pickle_data_to_shelve(pickle_filename, shelf_filename):
        """
        convert a file of pickle data (pickle_filename) 
        into a new shelve file (shelf_filename).
        """
        log.info('Pickle->Shelve: open pickle file')
        pickle_data = None  # Define here to establish scope
        with open(pickle_filename, 'rb') as pickle_io:
            pickle_data = pickle.load(pickle_io)

        log.info('Pickle->Shelve: create a shelf file')
        shelf_database = shelve.open(shelf_filename)

        log.info('Pickle->Shelve: save the pickle data to the shelf file')
        shelf_database['key'] = pickle_data

        log.info('Pickle->Shelve: close the shelf file')
        shelf_database.close()

        log.info('Pickle->Shelve: open the shelf file again')
        shelf_db = shelve.open(shelf_filename)

        log.info('Pickle->Shelve: read the shelf data')
        shelf_data = shelf_db['key']

        log.info('Pickle->Shelve: are pickle and shelf data identical?')
        print(f'Pickle/Shelve data comparison: {pickle_data == shelf_data}')

        log.info('Pickle->Shelve: close the shelf file again')
        shelf_db.close()

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

    save_pickle_file(all_planes, '../data/pickle_planes.pkl')
    load_pickle_file('../data/pickle_planes.pkl')
    convert_pickle_data_to_shelve('../data/pickle_planes.pkl',
                                  '../data/shelf_planes')

    return
