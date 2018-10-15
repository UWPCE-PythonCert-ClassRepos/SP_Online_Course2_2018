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

    def my_data_example():
        log.info("Step 20: Create some data for pickling, at least 10 rows with 5 fields each")
        write_data = list()
        write_data.append(["Apollo 7", "Wally Schirra", "Walt Cunningham", "Donn Eisele", "10/11/1968", "10/22/1968"])
        write_data.append(["Apollo 8", "Frank Borman", "James Lovell", "William Anders", "12/12/1968", "12/27/1968"])
        write_data.append(["Apollo 9", "James McDivitt", "David Scott", "Russell Schweickart", "3/3/1969", "3/13/1969"])
        write_data.append(["Apollo 10", "Thomas Stafford", "John Young", "Eugene Cernan", "5/18/1969", "5/26/1969"])
        write_data.append(["Apollo 11", "Neil Armstrong", "Michael Collins", "Buzz Aldrin", "7/16/1969", "7/24/1969"])
        write_data.append(["Apollo 12", "Charles Conrad", "Richard Gordon", "Alan Bean", "11/14/1969", "11/24/1969"])
        write_data.append(["Apollo 13", "James Lovell", "Jack Swigert", "Fred Haise", "4/11/1970", "4/17/1970"])
        write_data.append(["Apollo 14", "Alan Shepard", "Stuart Roosa", "Edgar Mitchell", "1/31/1971", "2/9/1971"])
        write_data.append(["Apollo 15", "David Scott", "Alfred Worden", "James Irwin", "7/26/1971", "8/7/1971"])
        write_data.append(["Apollo 16", "John Young", "Thomas Mattingly", "Charles Duke", "4/16/1972", "4/27/1972"])
        write_data.append(["Apollo 17", "Eugene Cernan", "Ronald Evans", "Harrison Schmitt", "12/7/1972", "12/19/1972"])

        log.info("Step 21: Pickling!")
        with open("../data/apollo.pkl", "wb") as apollo_file:
            pickle.dump(write_data, apollo_file)

        log.info("Step 22: Pickle complete, now read it back")
        read_data = None
        with open("../data/apollo.pkl", "rb") as apollo_file:
            read_data = pickle.load(apollo_file)

        if write_data == read_data:
            log.info("Step 23: Compared the written and read data, and they data match!")
        else:
            log.info("Step 23: Compared the written and read data, and they DO NOT match.")

        log.info("Step 24: Now convert it to a shelf.")
        shelf_file = shelve.open('../data/apollo_shelf.dat')
        shelf_file['7'] = write_data[0]
        shelf_file['8'] = write_data[1]
        shelf_file['9'] = write_data[2]
        shelf_file['10'] = write_data[3]
        shelf_file['11'] = write_data[4]
        shelf_file['12'] = write_data[5]
        shelf_file['13'] = write_data[6]
        shelf_file['14'] = write_data[7]
        shelf_file['15'] = write_data[8]
        shelf_file['16'] = write_data[9]
        shelf_file['17'] = write_data[10]

        log.info("Step 25: Shelf saved, now retrieve an Apollo mission by number.")
        apollo_13 = shelf_file['13']
        if apollo_13 == write_data[6]:
            log.info("Successfully retrieved Apollo 13!")
        else:
            log.info("FAILED to retrieve Apollo 13.")

    run_pickle()
    run_shelve()
    run_csv()
    run_json()
    my_data_example()

    return
