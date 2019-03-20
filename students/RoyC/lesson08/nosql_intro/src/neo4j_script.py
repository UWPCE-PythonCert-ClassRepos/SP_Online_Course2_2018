"""
    neo4j example
"""


import utilities
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def run_example():

    log.info('Step 1: First, clear the entire database, so we can start over')
    log.info("Running clear_all")

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add a few people")

    with driver.session() as session:

        log.info('Adding a few Person nodes')
        log.info('The cyph language is analagous to sql for neo4j')
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Homer', 'Simpson'),
                            ('Marge', 'Simpson'),
                            ('Ned', 'Flanders'),
                            ('Moe', 'Szylak'),
                            ('Edna', 'Krabapple')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info("Step 3: Get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])

        log.info('Step 4: Create some relationships')
        log.info("Bob Jones likes Alice Cooper, Fred Barnes and Marie Curie")

        for first, last in [("Alice", "Cooper"),
                            ("Fred", "Barnes"),
                            ("Marie", "Curie")]:
            cypher = """
              MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
              CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              RETURN p1
            """ % (first, last)
            session.run(cypher)

        log.info("Step 5: Find all of Bob's friends")
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

        log.info("Setting up Marie's friends")

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

        print("Step 6: Find all of Marie's friends?")
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

        print("Step 7: add people's favorite colors")

        for color in ['orange']:
            cypher = """
              MATCH (p1:Person {first_name:'Homer', last_name:'Simpson'})
              CREATE (p1)-[favorite:FAVORITE]->(p2:Color {name:'%s'})
              RETURN p1
            """ % (color)
            session.run(cypher)

        for color in ['orange', 'blue']:
            cypher = """
              MATCH (p1:Person {first_name:'Marge', last_name:'Simpson'})
              CREATE (p1)-[favorite:FAVORITE]->(p2:Color {name:'%s'})
              RETURN p1
            """ % (color)
            session.run(cypher)

        for color in ['red', 'green']:
            cypher = """
              MATCH (p1:Person {first_name:'Ned', last_name:'Flanders'})
              CREATE (p1)-[favorite:FAVORITE]->(p2:Color {name:'%s'})
              RETURN p1
            """ % (color)
            session.run(cypher)

        for color in ['blue', 'green']:
            cypher = """
              MATCH (p1:Person {first_name:'Moe', last_name:'Szylak'})
              CREATE (p1)-[favorite:FAVORITE]->(p2:Color {name:'%s'})
              RETURN p1
            """ % (color)
            session.run(cypher)

        for color in ['yellow', 'red', 'pink']:
            cypher = """
              MATCH (p1:Person {first_name:'Edna', last_name:'Krabapple'})
              CREATE (p1)-[favorite:FAVORITE]->(p2:Color {name:'%s'})
              RETURN p1
            """ % (color)
            session.run(cypher)

        log.info("Step 8: For each color, list people that have it as at least one of their favorites")
        for color in ['orange', 'blue', 'red', 'green', 'yellow', 'pink']:
            cyph = """
                MATCH (c:Color)<-[:FAVORITE]-(p:Person) WHERE (c.name ='%s') RETURN p
                """ % (color)
            result = session.run(cyph)
            print(f"\nColor {color} is a favorite of these people:")
            for rec in result:
                for person in rec.values():
                    print(person['first_name'], person['last_name'])

        log.info("\nStep 9: List each persons favorite color")
        for first, last in [('Homer', 'Simpson'), ('Marge', 'Simpson'), ('Ned', 'Flanders'), ('Moe', 'Szylak'), ('Edna', 'Krabapple')]:
            cyph = """
                MATCH (p:Person {first_name:'%s', last_name:'%s'})-[:FAVORITE]->(colors) RETURN colors
                """ % (first, last)
            result = session.run(cyph)
            print(f"\nThe favorite colors for {first} {last} are:")
            for rec in result:
                for color in rec.values():
                    print(color['name'])
