"""
    neo4j example
"""

import neo4j

from login_database import login_neo4j_cloud
from login_database import get_credentials

def run_example():

    # First, clear the entire database, so we can start over

    credentials = login_database.get_credentials('neo4j_cloud')

    print("Running clear_all")

    with driver.session() as session:
        print("Before clearing: all the records")
        result = session.run("MATCH (n) RETURN n")
        msg = ("There are these records:" +
               "\n".join([str(rec) for rec in result]))
        session.run("MATCH (n) DETACH DELETE n")

    """
    Add a few people, some with a little more info
    """
    with driver.session() as session:

        print('Adding a few Person nodes')
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (first, last)
            session.run(cyph)

        print("\nHere are all of people in the DB now:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        for record in result:
            print(record['first_name'], record['last_name'])

        print('\nCreate some relationships')
        # Bob Jones likes Alice Cooper, Fred Barnes and Marie Curie

        for first, last in [("Alice", "Cooper"),
                            ("Fred", "Barnes"),
                            ("Marie", "Curie")]:
            cypher = """
              MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)
            session.run(cypher)

        print("Can we find all of Bob's friends?")
        cyph = """
          MATCH (bob {first_name:'Bob', last_name:'Jones'})
                -[:FRIEND]->(bobFriends)
          RETURN bobFriends
          """
        result = session.run(cyph)
        print("Bob's friends are:")
        for rec in result:
            for f in rec.values():
                print(f['first_name'], f['last_name'])

        print("\nSetting up Marie's friends")

        for first, last in [("Mary", "Evans"),
                            ("Alice", "Cooper"),
                            ('Fred', 'Barnes'),
                            ]:
            cypher = """
              MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)
            # print(cypher)
            session.run(cypher)

        print("Can we find all of Marie's friends?")
        cyph = """
          MATCH (marie {first_name:'Marie', last_name:'Curie'})
                -[:FRIEND]->(friends)
          RETURN friends
          """
        result = session.run(cyph)
        print("Marie's friends are:")
        for rec in result:
            for f in rec.values():
                print(f['first_name'], f['last_name'])

