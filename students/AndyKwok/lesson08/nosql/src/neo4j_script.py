"""
    neo4j example
"""

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
                
def run_nosql_ex():

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    with driver.session() as session:
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Tester_1','A'),
                            ('Tester_2','B'),
                            ('Tester_3','C')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)
            
        for color in [('Blue'),
                      ('Red'),
                      ('Black'),
                      ('Yellow'),
                      ('Green'),
                      ]:
            cyph = "CREATE (n:Color_1 {each_color: '%s'})" % (color)
            session.run(cyph)            

        for first, last, color in [('Bob', 'Jones', 'Red'),
                            ('Nancy', 'Cooper', 'Blue'),
                            ('Alice', 'Cooper', 'Red'),
                            ('Fred', 'Barnes', 'Yellow'),
                            ('Mary', 'Evans', 'Black'),
                            ('Marie', 'Curie', 'Red'),
                            ('Tester_1','A', 'Green'),
                            ('Tester_2','B', 'Yellow'),
                            ('Tester_3','C', 'Red')
                            ]:
            cypher_person = """
              MATCH (p1:Person {first_name:'%s', last_name:'%s'})
              CREATE (p1)-[person_rel:PERSON_REL]->(p2:Color {favorite_color:'%s'})
              RETURN p1
            """ % (first, last, color)
            cypher_color = """
              MATCH (p3:Color_1 {each_color:'%s'})
              CREATE (p3)-[color_rel:COLOR_REL]->(p1:Person {first_name:'%s', last_name:'%s'})
              RETURN p3
            """ % (color, first, last)            
            session.run(cypher_person)
            session.run(cypher_color)

        cyph = """
          MATCH (red {each_color:'Red'})
                -[:COLOR_REL]->(individual)
          RETURN individual
          """
        result = session.run(cyph)
        print("Here are the people who likes red:")
        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])
                
        cyph = """MATCH (p:Person)
                        -[:PERSON_REL]->(color)
                  RETURN p.first_name as first_name, p.last_name as last_name, color as color
                """
        result = session.run(cyph)
        print("The following shows everyone's favorite_color:")
        for record in result:
            print(record['first_name'] + " " + record['last_name'] + " likes " + record['color']['favorite_color'])
