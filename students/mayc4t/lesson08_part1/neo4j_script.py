"""Self-contained neo4j example."""

import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

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


def run_neo4j_example():
    """Neo4j example from course, extended as needed for lesson08."""

    print('\nStep 1: First, clear the entire database, so we can start over')

    driver = login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    with driver.session() as session:

        print('\nStep 2: Add a few people')
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        print('\nStep 3: Get all of people in the DB:')
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
               """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])

        print('\nStep 4: Create some relationships')
        print("Bob Jones likes Alice Cooper, Fred Barnes and Marie Curie")

        for first, last in [("Alice", "Cooper"),
                            ("Fred", "Barnes"),
                            ("Marie", "Curie")]:
            cypher = """
              MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)
            session.run(cypher)

        print("\nStep 5: Find all of Bob's friends")
        cyph = """
          MATCH (bob {first_name:'Bob', last_name:'Jones'})
                -[:FRIEND]->(bobFriends)
          RETURN bobFriends
          """
        result = session.run(cyph)
        print("Bob's friends are:")
        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])

        print("\nStep 6: Add Marie's friends and find them.")
        for first, last in [("Mary", "Evans"),
                            ("Alice", "Cooper"),
                            ('Fred', 'Barnes'),
                            ]:
            cypher = """
              MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)
            session.run(cypher)

        cyph = """
          MATCH (marie {first_name:'Marie', last_name:'Curie'})
                -[:FRIEND]->(friends)
          RETURN friends
          """
        result = session.run(cyph)
        print("\nMarie's friends are:")
        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])


if __name__ == '__main__':
    run_neo4j_example()
