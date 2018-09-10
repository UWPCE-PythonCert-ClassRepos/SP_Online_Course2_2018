#!/usr/bin/env

import mailroom5

import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth
import model

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

driver = None


def login_neo4j_cloud():
    """Connect to neo4j and login."""

    try:
        config.read(config_file)
        user = config["neo4j_cloud"]["user"]
        pw = config["neo4j_cloud"]["pw"]
        print(f'Got user=***** pw=***** from {config_file}')
    except Exception as e:
        print(f'Error parsing {config_file}: {e}')

    url = 'bolt://hobby-aghpmhoaabhjgbkemfjekpbl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(url, auth=basic_auth(user, pw))

    return driver

def init_donors_db():
    global driver

    driver = login_neo4j_cloud()

    # initiliaze donors_db here
    # ...
    db_present = False

    # First, check whether the database exists
    with driver.session() as session:
        #session.run("MATCH (n) DETACH DELETE n")
        #raise NotImplemented('Implement me!')

        cyph = """MATCH (p:Person)
                  RETURN p.name as name
               """
        result = session.run(cyph)
        for record in result:
            db_present = True
            break

    if db_present:
        donors = []
        with driver.session() as session:
            cyph = """MATCH (p:Person)
                      RETURN p.name as name
                   """
            result = session.run(cyph)
            for record in result:
                name = record['name']

                cyph = """
                    MATCH (person {name:'%s'})
                          -[:DONATION]->(donation)
                    RETURN donation
                """ % (name)
                result_nested = session.run(cyph)
                donations = []
                for record_nested in result_nested:
                    for donation in record_nested.values():
                        donations.append(int(donation['donation']))

                sub_names = name.split(',')
                last = sub_names[0]
                first = None
                if len(sub_names) > 1:
                    first = sub_names[1]
                d = mailroom5.Donor(first, last,
                                    recorded_donation_list=donations)
                donors.append(d)

        donors_db = mailroom5.Donor_DB(donors)
    else:
        d1 = mailroom5.Donor("__Kate", "Spade", [100])
        d2 = mailroom5.Donor("__Michael", "Kors", [100, 200])
        d3 = mailroom5.Donor("__Tory", "Burch", [100, 200, 300])
        d4 = mailroom5.Donor("__Stuart", "Weitzman", [100, 200, 300, 400])
        d5 = mailroom5.Donor("__Kate", "Summerville", [100, 200, 300, 400, 500])
        donors_db = mailroom5.Donor_DB([d1, d2, d3, d4, d5])

    return donors_db


def SaveDonorInfo(first_name, last_name):
    name = last_name + ',' + first_name
    with driver.session() as session:
        found_name = False
        cyph = """
            MATCH (p:Person {name: '%s'})
            RETURN p.name as name
        """ % (name)
        result = session.run(cyph)
        for record in result:
            found_name = True

        if not found_name:
            cyph = "CREATE (n:Person {name: '%s', first:'%s', last: '%s'})" % (
                name, first_name, last_name)
            session.run(cyph)


def SaveDonation(name, donation):
    with driver.session() as session:
        cypher = """
            MATCH (p:Person {name:'%s'})
            CREATE (p)-[donation:DONATION]->(d:Donation {donation:'%s'})
            RETURN p
        """ % (name, donation)
        session.run(cypher)


def UpdateDonation(name, old_donation, new_donation):
    if new_donation:
        with driver.session() as session:
            cypher = """
                MATCH (d:Donation)<-[donation:DONATION]-(p:Person)
                WHERE p.name='%s'
                AND d.donation='%s'
                SET d.donation = '%s'
            """ % (name, old_donation, new_donation)
            session.run(cypher)
    else:
        with driver.session() as session:
            cypher = """
                MATCH (d:Donation)<-[donation:DONATION]-(p:Person)
                WHERE p.name='%s'
                AND d.donation='%s'
                DETACH DELETE d
            """ % (name, old_donation)
            session.run(cypher)


if __name__ == "__main__":
    model.SaveDonorInfo = SaveDonorInfo
    model.SaveDonation = SaveDonation
    model.UpdateDonation = UpdateDonation

    donors_db = init_donors_db()
    mailroom5.enter_main_loop(donors_db)
