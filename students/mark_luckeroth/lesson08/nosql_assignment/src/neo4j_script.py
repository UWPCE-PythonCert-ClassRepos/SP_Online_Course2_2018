"""
    neo4j example
"""


import utilities
import login_database
import utilities
import random

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
####################################################################################################################
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
##################################################################################################################3
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

        log.info('Step 7: Adding a few new Person nodes')
        for first, last in [('Curious', 'George'),
                            ('Man', 'Yellowhat'),
                            ('Professor', 'Wiseman'),
                            ('Bill', 'Neighbor'),
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info('Step 8: Adding colors')
        color_list = ['Cyan', 'Amaranth', 'Burgundy', 'Coral', 'Mauve',
                        'Olive', 'Periwinkle', 'Taupe', 'Ultramarine']
        for color_name in color_list:
            cyph = "CREATE (n:Color {name: '%s'})" % (color_name)
            session.run(cyph)

        log.info('Step 9: Assign favorite colors')
        log.info("Get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        people = session.run(cyph)
        log.info("assign 2 fav colors")
        for first, last in [("Curious", "George"),
                            ("Professor", "Wiseman"),
                            ('Bill', 'Neighbor'),
                            ]:
            first_color = random.choice(color_list)
            cypher = """
              MATCH (p1:Person {first_name:'%s', last_name:'%s'})
              CREATE (p1)-[favorite:FAVORITE]->(c:Color {name:'%s'})
              RETURN p1
            """ % (first, last, first_color)
            session.run(cypher)
            second_color = random.choice(color_list)
            cypher = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[favorite:FAVORITE]->(c:Color {name:'%s'})
              RETURN p
            """ % (first, last, second_color)
            session.run(cypher)

        log.info('Step 10: print all people for each favorite color')
        for color in color_list:
            cyph = """
              MATCH (people)
                    -[:FAVORITE]->(color {name:'%s'})
              RETURN people
              """% (color)
            result = session.run(cyph)
            print("\nThe people who like %s are:"%(color))
            for rec in result:
                for person in rec.values():
                    print(person['first_name'], person['last_name'])

        log.info('Step 11: print all colors for each person')
        for first, last in [("Curious", "George"),
                            ("Professor", "Wiseman"),
                            ('Bill', 'Neighbor'),
                            ]:
            cyph = """
              MATCH (person {first_name:'%s', last_name:'%s'})
                    -[:FAVORITE]->(colors)
              RETURN colors
              """% (first, last)
            result = session.run(cyph)
            print("\n '%s' '%s' likes the following colors:"%(first, last))
            for rec in result:
                for color in rec.values():
                    print(color['name'])