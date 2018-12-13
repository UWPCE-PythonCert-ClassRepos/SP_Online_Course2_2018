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

    def run_csv():
        """
        write and read a csv
        """
        log.info("\n\n====")
        peopledata = [
            ('John', 'second guitar', 117.45, 'Engineer', '55'),
            ('Paul', 'bass', 22.01, 'Nurse', 30),
            ('George', 'lead guitar', 45.99, 'Firefighter', 45),
            ('Ringo', 'drume', 77.0, 'Cashier', 23),
            ('Roger', 'vocals', 12.5, 'Librarian', 37),
            ('Keith', 'drums', 6.25, 'Teacher', 43),
            ('Pete', 'guitar', 0.1, 'Doctor', '60'),
            ('John', 'bass', 89.71, 'Carpenter', 65),
            ('Amy', 'violin', 89.71, 'Accountant', 35),
            ('Max', 'piano', 89.71, 'Pilot', 51)
        ]
        log.info("Step 8: Write csv file")
        with open('../data/cindy_db.csv', 'w') as people:
            peoplewriter = csv.writer(people)
            peoplewriter.writerow(peopledata)

        log.info("Step 9: Read csv file back")
        with open('../data/cindy_db.csv', 'r') as people:
            people_reader = csv.reader(people, delimiter=',', quotechar='"')
            for row in people_reader:
                pprint.pprint(row)

    run_csv()

    return
