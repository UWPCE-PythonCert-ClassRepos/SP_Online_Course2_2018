#!/usr/bin/env python3

import configparser
from pathlib import Path
import pprint
import pymongo

config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()

def login_mongodb_cloud():
    """
        connect to mongodb and login
    """

    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]

    except Exception as e:
        print(f'error: {e}')

    client = pymongo.MongoClient(f'mongodb://{user}:{pw}'
                                 '@cindymongodb-shard-00-00-stkwh.mongodb.net:27017,cindymongodb-shard-00-01-stkwh.mongodb.net:27017,cindymongodb-shard-00-02-stkwh.mongodb.net:27017/test?ssl=true&replicaSet=cindyMongodb-shard-0&authSource=admin&retryWrites=true')

    return client

client = login_mongodb_cloud()

class Donor:

    def __init__(self, name, list_donations):
        self._name = name
        self._list_donations = list_donations
        self._donation_count = len(list_donations)
        self._amount = sum(list_donations)


    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def add(self, donation_amount):
        self._amount +=donation_amount
        self._donation_count += 1
        self._list_donations.append(donation_amount)


    @property
    def donation_count(self):
        return self._donation_count

    @property
    def average(self):
        return self._amount / self._donation_count

    def get_letter_text(self, name, amount):
        msg = []
        msg.append('Dear {},'.format(name))
        msg.append('\n\n\tThank you for your very kind donation of ${:.2f}.'.format(amount))
        msg.append('\n\n\tIt will be put to very good use.')
        msg.append('\n\n\t\t\t\tSincerely,')
        msg.append('\n\t\t\t\t-The Team\n')
        return "".join(msg)

    def __lt__(self, other):
        return self._amount < other._amount

    def __gt__(self, other):
        return self._amount > other._amount

    def __eq__(self, other):
        return self._amount == other._amount

class Donations:

    def __init__(self):
        """collection of donors"""
        self._donors = {}

    def insert_donor(self, donor):
        self._donors[donor.name] = donor

    def add_update(self, donor):
        """ add or update donor"""

        total_amount = donor._amount
        num_of_donation = donor._donation_count
        # existing donor
        if donor.name in self._donors.keys():
            d =self._donors[donor.name]
            # update donation amount
            d.add(donor.amount)
            total_amount = d._amount
            num_of_donation = d._donation_count
        else:
            # new donor
            self._donors[donor.name] = donor


        db = client['mailroom']
        donors_db = db['donations']

        average = total_amount/num_of_donation

        donors_db.collection.update(
            {'name':donor.name},
            {
                '$set':{'total_amount': total_amount,
                    'donation_count':num_of_donation,
                    'donation_average':average}
            },
            upsert=True)

    def delete(self, donor_name):
        """ delete a donor from database"""

        if donor_name in self._donors:
            self._donors.pop(donor_name)
        try:

            db = client['mailroom']
            donors_db = db['donations']

            query = {'name': {'$eq':donor_name}}
            donors_db.collection.remove(query)
        except Exception as e:
            print("exception occurred")
            print(e)

    @property
    def donors(self):
        return self._donors

    def generate_report(self):
        """Get data from database and Generate report"""

        report = []
        report.append("--------------------------------------------------------------")
        msg = "{:20} | {:10} | {:5} | {:10}".format('Donor Name', 'Total Given', 'Num Gifts', 'Average Gift')
        report.append(msg)
        report.append("--------------------------------------------------------------")

        db = client['mailroom']
        donors_db = db['donations']
        results = donors_db.collection.find({})
        for donor in results:
            name = donor['name']
            total_amount = donor['total_amount']
            donation_count = donor['donation_count']
            average = donor['donation_average']

            a_row = '{:20}  $ {:>10.2f}  {:>10d}  $ {:>11.2f}'.format(name,
                                                                      total_amount,
                                                                      donation_count,
                                                                      average)
            report.append(a_row)

        return "\n".join(report)
