
import pprint
import login_database
import utilities
from pathlib import Path
import os
import pymongo 
from pymongo import MongoClient
import configparser


log = utilities.configure_logger('default', '../logs/mongodb_script.log')
config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


donors = [{'donor': 'Bill Gates',
          'donations': 6000},
          {'donor': 'Jeff Bezos',
           'donations': 10000},
          {'donor': 'Hannah Smith',
           'donations': 60000},
          {'donor': 'John Clark',
           'donations': 3000},
          {'donor': 'Andrew Jones',
           'donations': 8000}]

def run_mongodb():
    with login_database.login_mongodb_cloud() as client:
        db = client['mailroom'] 
        donations = db['donations']
        donations = donations.insert_many(donors)
        print(donations.inserted_ids)
        query = {'donations': 10000}

        donations.find_one(query)


if __name__ == '__main__':
    run_mongodb()
   





