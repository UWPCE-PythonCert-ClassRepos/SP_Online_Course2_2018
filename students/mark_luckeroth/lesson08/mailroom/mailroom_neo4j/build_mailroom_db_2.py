"""
    Lesson 08 mailroom neo4j assignment
    build baseline database
"""

import logging
import login_database
import pprint
import initial_donor_data

def populate_donordata():
    """
    add person data to database
    """

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    log.info('Build Donor Database')

    log.info('Step 1: First, clear the entire database, so we can start over')
    log.info("Running clear_all")

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add donors")
    donor_names = ['Peter Pan', 'Paul Hollywood', 'Mary Berry',
                    'Jake Turtle', 'Raja Koduri']
    donations = [[10., 10., 10., 10.],
                [5., 5000., 5., 5.],
                [100.],
                [123., 456., 789.],
                [60., 60000.]]
    with driver.session() as session:
        for i, name in enumerate(donor_names):
            for amount in donations[i]:
                cyph = "CREATE (n:Person {name:'%s', amount:'%s'})" % (name, amount)
                session.run(cyph)

        log.info("Step 3: Get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.name as name, p.amount as amount
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print('{} has donated ${:.2f}'.format(record['name'], float(record['amount'])))
####################################################################################################################
        log.info("Step 4: Now get donation list by donor name")
        for name in donor_names:
            cyph = """MATCH (p:Person {name: '%s'})
                      RETURN p.name as name, p.amount as amount""" % (name)
            result = session.run(cyph)
            donations = []
            for record in result:
                donations.append(float(record['amount']))
            print('{} made the following donations {}'.format(name, ''.join(str(donations))))


        log.info('Step 5: Reset a name')
        cyph = """MATCH (p:Person {name: 'Paul Hollywood'})
                  SET p.name = 'Mark Luckeroth'
                  RETURN p.name as name, p.amount as amount"""
        result = session.run(cyph)
        for record in result:
            print('{} has donated ${:.2f}'.format(record['name'], float(record['amount'])))

if __name__ == '__main__':
    populate_donordata()
