"""
My simple CSV baseball teams script
"""

import csv
import pprint

import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

def run_csv():
    """
    write and read a csv
    """
    log.info("\nStep 1: define baseball team data")
    baseball_teams = [
        ('Mariners', 'Seattle', 'blue/teal'),
        ('Angels', 'Anaheim', 'red'),
        ('Athletics', 'Oakland', 'green/yellow'),
        ('Rangers', 'Texas', 'blue/red'),
        ('Giants', 'San Francisco', 'orange/black'),
        ('Dodgers', 'Los Angeles', 'blue'),
        ('Padres', 'San Diego', 'brown/yellow'),
        ('Diamondbacks', 'Arizona', 'red/teal')
    ]
    log.info("Step 2: Write csv file")
    with open('../data/baseball_teams.csv', 'w') as bball_teams:
        bball_writer = csv.writer(bball_teams)
        bball_writer.writerow(baseball_teams)

    log.info("Step 9: Read csv file back")
    with open('../data/baseball_teams.csv', 'r') as bball_teams:
        bball_reader = csv.reader(bball_teams, delimiter=',', quotechar='"')
        for row in bball_reader:
            pprint.pprint(row)

