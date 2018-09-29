#!/usr/bin/env

import mailroom5

import configparser
from pathlib import Path
import redis
import model

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

redis_client = None


def login_redis_cloud():
    """Connect to redis and login."""

    try:
        config.read(config_file)
        host = config["redis_cloud"]["host"]
        port = config["redis_cloud"]["port"]
        pw = config["redis_cloud"]["pw"]
        print(f'Got host={host} port={port} pw=***** from {config_file}')
    except Exception as e:
        print(f'Error parsing {config_file}: {e}')

    try:
        r = redis.StrictRedis(host=host, port=port, password=pw,
                              decode_responses=True)
    except Exception as e:
        print(f'Error connecting to Redis DB: {e}')

    return r


def init_donors_db():
    global redis_client

    # initiliaze donors_db here
    # ...
    db_present = False

    # First, check whether the database exists
    try:
        redis_client = login_redis_cloud()
        if redis_client.dbsize():
            db_present = True
    except Exception as e:
        print(f'Redis error: {e}')

    if db_present:
        donors = []
        keys = redis_client.keys('*')
        for name in keys:
            sub_names = name.split(',')
            last = sub_names[0]
            first = None
            if len(sub_names) > 1:
                first = sub_names[1]
            donations = [int(donation) for donation in redis_client.lrange(name, 0, -1)]

            d = mailroom5.Donor(first, last,
                                recorded_donation_list=donations)
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
    global redis_client

    redis_client.rpush(name, donation)


def UpdateDonation(name, old_donation, new_donation):
    if new_donation:
        donations = [int(donation) for donation in redis_client.lrange(name, 0, -1)]
        idx = donations.index(old_donation)
        redis_client.lset(name, idx, new_donation)
    else:
        redis_client.lrem(name, -1, old_donation)



if __name__ == "__main__":
    model.SaveDonorInfo = SaveDonorInfo
    model.SaveDonation = SaveDonation
    model.UpdateDonation = UpdateDonation

    mailroom5.donors_db = init_donors_db()
    mailroom5.enter_main_loop()
