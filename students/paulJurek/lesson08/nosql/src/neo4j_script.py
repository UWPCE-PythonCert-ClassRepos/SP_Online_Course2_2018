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
                            ('Bob', 'Dylan'),
                            ('Santa', 'Claus')
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

        log.info('Step 7: add colors to database')
        colors_2_create = ['red', 'blue', 'green', 'white', 'black']
        for color in colors_2_create:
          cyph = "CREATE (n:Color {name:'%s'})" % (color)
          session.run(cyph)

        log.info("Step 8: Get all of colors in the DB:")
        cyph = """MATCH (p:Color)
                  RETURN p.name as color_name
                """
        result = session.run(cyph)
        print("Colors in database:")
        for record in result:
            print(record['color_name'])

        log.info('Step 9: Build color relationship')
        log.info("Bob Jones likes black and white")

        for first, last, color in [("Bob", "Jones", "black"),
                            ("Bob", "Jones", "white"),
                            ("Fred", "Barnes", "blue"),
                            ("Marie", "Curie", "red")]:
            cypher = """
              MATCH (p1:Person {first_name:'%s', last_name:'%s'})
              CREATE (p1)-[color:COLOR]->(c1:Color {color_name:'%s'})
              RETURN p1
            """ % (first, last, color)
            session.run(cypher)

        log.info('Step 10: Report people who like each color')
        colors = ['red', 'blue', 'green', 'white', 'black']
        for color in colors:
          cyph = """
            MATCH (color {color_name:'%s'})
                  -[:PERSON]->(friends)
            RETURN friends
            """
          result = session.run(cyph)
          print(f'people who like {color}')
          for rec in result:
              for friend in rec.values():
                  print(friend['first_name'], friend['last_name'])
        
