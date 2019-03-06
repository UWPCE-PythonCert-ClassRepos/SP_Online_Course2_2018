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
        teamdata = [
            ('Oklahoma State', 'Coyboys', 52, 'Stillwater', 'Orange'),
            ('Texas', 'Longhorns', 44, 'Austin', 'Orangish Brown'),
            ('Oklahoma', 'Sooners', 29, 'Norman', 'Red'),
            ('West Virginia', 'Mountaineers', 19, 'Morgantown', 'Blue'),
            ('Iowa State', 'Cyclones', 13, 'Red'),
            ('Kansas', 'Jayhawks', 11, 'Lawrence', 'Blue'),
            ('TCU', 'Horned Frogs', 4, 'Fort Worth', 'Purple'),
            ('Baylor', 'Bears', 3, 'Waco', 'Green'),
            ('Texas Tech', 'Red Raiders' , 1, 'Lubbock', 'Red'),
            ('Kansas State', 'Wildcats', 0, 'Manhattan', 'Purple')
        ]
        log.info("Step 1: Write csv file")
        with open('../data/big12.csv', 'w') as schools:
            peoplewriter = csv.writer(schools)
            peoplewriter.writerow(teamdata)

        log.info("Step 2: Read csv file back")
        with open('../data/big12.csv', 'r') as schools:
            school_reader = csv.reader(schools, delimiter=',', quotechar='"')
            for row in school_reader:
                pprint.pprint(row)

    run_csv()

    return
