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
        log.info("Working with csv data: name, role, age, yrs exp., degree?")
        peopledata = [
            ('Luke', 'bass', 29, 15, 'yes'),
            ('Virgil', 'lead singer', 15, 8, 'no'),
            ('River', 'lead guitar', 36, 20, 'yes'),
            ('Joseph', 'cello', 20, 12, 'no'),
            ('Kibson', 'vocals & keyboard', 12.5, 7, 'no'),
            ('Dexter', 'accordion', 55, 45, 'yes'),
            ('China', 'drums', 22, 17, 'no'),
            ('Lucy', 'cowbell', 41, 29, 'no'),
            ('Percy', 'security', 35, 3, 'no'),
            ('Beckett', 'merch sales', 27, 1, 'yes')
        ]
        log.info("Step 8: Write csv file")
        with open('../data/rockband.csv', 'w') as people:
            peoplewriter = csv.writer(people)
            peoplewriter.writerow(peopledata)

        log.info("Step 9: Read csv file back")
        with open('../data/rockband.csv', 'r') as people:
            people_reader = csv.reader(people, delimiter=',', quotechar='"')
            for row in people_reader:
                pprint.pprint(row)

    run_csv()

    return
