#!/usr/bin/env python3

import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth

config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


def login_neo4j_cloud():
    """
        connect to neo4j and login

    """

    config.read(config_file)

    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-dlifcjbocggfgbkemghfhgcl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver

driver = login_neo4j_cloud()

class Donor:

    def __init__(self, name, donation_count, total_amount):
        self._name = name
        self._donation_count = donation_count
        self._amount = total_amount


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
        with driver.session() as session:

            cyph = """MATCH (d:Donor)
                  RETURN d
                """
            result = session.run(cyph)

            for record in result:
                for donor in record.values():
                    name = donor['name']
                    total_amount = donor['total_amount']
                    donation_count = donor['donation_count']
                    average = donor['average']
                    d = Donor(name, int(donation_count), float(total_amount))
                    self._donors[name] = d


    def insert_donor(self, donor):
        self._donors[donor.name] = donor

    def add_update(self, donor):
        """ add or update donor"""

        total_amount = donor._amount
        num_of_donation = donor._donation_count
        is_donor_new = True
        # existing donor
        if donor.name in self._donors.keys():
            d =self._donors[donor.name]
            # update donation amount
            d.add(donor.amount)
            total_amount = d._amount
            num_of_donation = d._donation_count
            is_donor_new = False
        else:
            # new donor
            self._donors[donor.name] = donor
            is_donor_new = True

        average = total_amount/num_of_donation

        if is_donor_new == True:
            # add new donor


            my_dict = { 'total_amount':total_amount,
                    'donation_count': num_of_donation,
                    'donation_average':average}

            with driver.session() as session:
                cyph = "CREATE (d:Donor {name:'%s', total_amount: '%s',donation_count: '%s', average: '%s'})" % (donor.name, total_amount, num_of_donation, average)
                session.run(cyph)
        else:
            # update donor
            with driver.session() as session:
                cyph = "MATCH (n:Donor {name:'%s'}) RETURN id(n)" % (donor.name)
                result = session.run(cyph)
                record_id = result.single()[0]
                cyph = "MATCH (d:Donor) WHERE ID(d) = %s SET d.donation_count = %s, d.average = %s, d.total_amount = %s RETURN d" % (record_id, num_of_donation, average, total_amount )
                session.run(cyph)


    def delete(self, donor_name):
        """ delete a donor from database"""

        if donor_name in self._donors:
            self._donors.pop(donor_name)

        with driver.session() as session:
            cyph = """MATCH (d:Donor {name: '%s'})
                DELETE d
                """ % donor_name
            session.run(cyph)
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

        with driver.session() as session:

            cyph = """MATCH (d:Donor)
                  RETURN d
                """
            result = session.run(cyph)

            for record in result:
                for donor in record.values():
                    name = donor['name']
                    total_amount = donor['total_amount']
                    donation_count = donor['donation_count']
                    average = donor['average']

                    a_row = '{:20}  $ {:>10}  {:>10}  $ {:>11}'.format(name,
                                                                      total_amount,
                                                                      donation_count,
                                                                      average)
                    report.append(a_row)

            return "\n".join(report)
