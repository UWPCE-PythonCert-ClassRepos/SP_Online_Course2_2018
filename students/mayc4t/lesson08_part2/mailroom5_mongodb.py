#!/usr/bin/env

import mailroom5

import configparser
from pathlib import Path
import pymongo
import model

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

DATABASE_NAME = 'mailroom5'
COLLECTION_NAME = 'donors'
mongodb_client = None


def login_mongodb_cloud():
    """Connect to mongodb and login."""

    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]
        print(f'Got user=***** pw=***** from {config_file}')
    except Exception as e:
        print(f'Error parsing {config_file}: {e}')

    client = pymongo.MongoClient(f'mongodb+srv://{user}:{pw}'
                                 '@cluster0-np6jb.gcp.mongodb.net/test'
                                 '?retryWrites=true')

    return client


def init_donors_db():
    global mongodb_client

    # initiliaze donors_db here
    # ...
    db_present = False
    mongodb_client = login_mongodb_cloud() 

    # First, check whether the database exists
    db = mongodb_client[DATABASE_NAME]
    for collection in db.list_collections():
        if collection['name'] == COLLECTION_NAME:
            db_present = True

    if db_present:
        collection = db[COLLECTION_NAME]
        cursor = collection.find({})
        raw_donors = {}
        for doc in cursor:
            name = doc['name']
            first = doc['first']
            last = doc['last']
            donation = doc['donation']
            if name not in raw_donors:
                raw_donors[name] = {
                    'first': first,
                    'last': last,
                    'donations': []
                }
            raw_donors[name]['donations'].append(donation)

        print(raw_donors)
        donors = []
        for _, donor in raw_donors.items():
            d = mailroom5.Donor(donor['first'], donor['last'],
                                recorded_donation_list=donor['donations'])
            donors.append(d)
        donors_db = mailroom5.Donor_DB(donors)
    else:
        d1 = mailroom5.Donor("__Kate", "Spade", [100])
        d2 = mailroom5.Donor("__Michael", "Kors", [100, 100])
        d3 = mailroom5.Donor("__Tory", "Burch", [100, 100, 100])
        d4 = mailroom5.Donor("__Stuart", "Weitzman", [100, 100, 100, 100])
        d5 = mailroom5.Donor("__Kate", "Summerville", [100, 100, 100, 100, 100])
        donors_db = mailroom5.Donor_DB([d1, d2, d3, d4, d5])

    return donors_db


def SaveDonorInfo(first_name, last_name):
    pass


def SaveDonation(name, donation):
    global mongodb_client

    sub_names = name.split(',')
    last = sub_names[0]
    first = None
    if len(sub_names) > 1:
        first = sub_names[1]

    db = mongodb_client[DATABASE_NAME]
    donors = db[COLLECTION_NAME]
    donors.insert_one({
        'name': name,
        'first': first,
        'last': last,
        'donation': donation})


def UpdateDonation(name, old_donation, new_donation):
    db = mongodb_client[DATABASE_NAME]
    donors = db[COLLECTION_NAME]
    if new_donation:
        donors.find_one_and_update(
            {'name': name, 'donation': old_donation},
            {'$set': {'donation': new_donation}})
    else:
        donors.delete_one({'name': name, 'donation': old_donation})


if __name__ == "__main__":
    model.SaveDonorInfo = SaveDonorInfo
    model.SaveDonation = SaveDonation
    model.UpdateDonation = UpdateDonation

    mailroom5.donors_db = init_donors_db()
    mailroom5.enter_main_loop()
