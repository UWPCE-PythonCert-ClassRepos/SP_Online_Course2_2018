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
        applicant_info = [
            ('Steve Bob', '1111 1st AVE, Seattle, WA 98044', 'Software Engineer', 15, 'UW'),
            ('Bob Steve', '1112 2nd AVE, Seattle, WA 98044', 'Aerospace Engineer', 12, 'CWU'),
            ('Alice Cooper', '1113 3rd AVE, Seattle, WA 98044', 'Ceramic Engineer', 19, 'PLU'),
            ('Bob Cooper', '1114 4th AVE, Seattle, WA 98044', 'Geological Engineer', 25, 'Seattle University'),
            ('Aiden Ned', '1115 5th AVE, Seattle, WA 98044', 'Chemical Engineer', 5, 'Oregon State'),
            ('Albert Steven', '1116 6th AVE, Seattle, WA 98044', 'Electrical Engineer', 1, 'Ohio State'),
            ('Steven Al', '1117 7th AVE, Seattle, WA 98044', 'Coder', 8, 'Mizzou'),
            ('Bill Bowl', '1118 8th AVE, Seattle, WA 98044', 'IT', 9, 'Purdue'),
            ('Robert Bob', '1119 9th AVE, Seattle, WA 98044', 'Software Engineer', 11, 'Notre Dame'),
            ('Bob Ross', '1110 10th AVE, Seattle, WA 98044', 'Manager', 55, 'Princeton'),

        ]
        log.info("Step 1: Write csv file")
        with open('../data/applicants.csv', 'w') as applicants:
            csv_writer = csv.writer(applicants)
            csv_writer.writerow(applicant_info)

        log.info("Step 2: Read csv file back")
        with open('../data/applicants.csv', 'r') as applicants:
            csv_reader = csv.reader(applicants, delimiter=',', quotechar='"')
            for row in csv_reader:
                pprint.pprint(row)

    run_csv()

    return
