"""
Data to populate mailroom db
"""


import login_database
import utilities
import os
import db_ops
import json
import random


try:
    os.chdir('../logs')
except OSError:
    os.mkdirs('../logs')


log = utilities.configure_logger('default', '../logs/mailroom_neo4j.log')


def get_donors_data():
    """
    current donors
    :return:
    """

    log.info('Step 1: First, clear the entire database, so we can start over')
    log.info("Running clear_all")

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add a few donors")

    with driver.session() as session:
        donors = (
            "Jerry Seinfeld",
            "George Costanza",
            "Elaine Bennis",
            "Cosmo Kramer",
            "Newman"
        )
        donations = [
            100.33,
            1000.2,
            22.1,
            55.1,
            22.11,
            66.4,
            76.2
        ]
        for donor in donors:
            cyph = """CREATE (:Person {{donor_name: '{}'}})
            """.format(donor)
            session.run(cyph)
        log.info('Check if donors were added to db')
        cyph = """MATCH (person:Person)
                    RETURN person.donor_name as donor_name
        """
        results = session.run(cyph)

        log.info('Adding donations')

        for record in results:
            log.info(record['donor_name'])
        for donor in donors:
            # Every person made 3 donations
            for x in range(0,3):
                cyph = """
                    MATCH (person:Person {{donor_name: '{}'}})
                    CREATE (person)-[donated:DONATED]->(d:Donations {{amount: {}}})
                    RETURN person
                """.format(donor,
                           donations[random.randint(0, 6)]
                )
                session.run(cyph)

        log.info('Check if donations were added')

        cyph = """
        MATCH (person:Person)
        return person
        """
        results = session.run(cyph)
        all_donors = []
        for record in results:
            all_donors.append(record['person']['donor_name'])
        log.info('All Donors: {}'.format(all_donors))
        for donor in all_donors:
            cyph = """
            MATCH (person:Person {{donor_name: '{}'}})
            -[:DONATED]-> (donation_amount)
            RETURN donation_amount
            """.format(donor)
            results = session.run(cyph)
            for record in results:
                log.info('{} has donated: {}$'.format(
                    donor,
                    record['donation_amount']['amount']
                ))

def start_db():
    """
    connect to mongodb and populate the data
    :return:
    """
    get_donors_data()


if __name__ == '__main__':
    # start_db()
    # db_ops.update_donations('Jerry Seinfeld', 500)
    # db_ops.list_donors()
    # db_ops.get_total_for_donor('Jerry Seinfeld')