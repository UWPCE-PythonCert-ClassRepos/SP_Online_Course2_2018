#!/usr/bin/env python3

import configparser
from pathlib import Path
import redis

config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


def login_redis_cloud():
    """
        connect to redis and login
    """

    config.read(config_file)
    host = config["redis_cloud"]["host"]
    port = config["redis_cloud"]["port"]
    pw = config["redis_cloud"]["pw"]

    r = redis.StrictRedis(host=host, port=port, password=pw, decode_responses=True)

    return r

client = login_redis_cloud()


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

        average = total_amount/num_of_donation

        my_dict = { 'total_amount':total_amount,
                    'donation_count': num_of_donation,
                    'donation_average':average}

        client.hmset(donor.name, my_dict)

        #print(client.hgetall(donor.name))

    def delete(self, donor_name):
        """ delete a donor from database"""

        if donor_name in self._donors:
            self._donors.pop(donor_name)
        try:

            client.delete(donor_name)
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

        for k, donor in self._donors.items():

            name = donor.name
            my_dict = client.hgetall(donor.name)
            print(my_dict)
            total_amount = my_dict['total_amount']
            donation_count = my_dict['donation_count']
            average = my_dict['donation_average']
            a_row = '{:20}  $ {:>10}  {:>10}  $ {:>11}'.format(name,
                                                                      total_amount,
                                                                      donation_count,
                                                                      average)
            report.append(a_row)

        return "\n".join(report)
