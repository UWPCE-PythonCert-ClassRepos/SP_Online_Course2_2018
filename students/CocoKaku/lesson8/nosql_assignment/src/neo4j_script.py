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

def run_exercise():
    """
    redis exercise

    Assignment:
    Add some new people to the database.
    Then add some colors.
    Create associations between people and their favorite colors
        (they can have more than one).
    Then list all of the people who have each color as their favorite.
    Can you also list all of the everyones favorite colors?
    """

    log.info('Step 1: First, clear the entire database, so we can start over')
    log.info("Running clear_all")
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add people to database")
    with driver.session() as session:
        for first, last in [('Bob', 'Jones'),
                            ('Marie', 'Curie'),
                            ('Leonardo', 'Davinci'),
                            ('Ansel', 'Adams'),
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (first, last)
            session.run(cyph)

        log.info("Step 2a: Check people in the DB")
        cyph = "MATCH (p:Person) RETURN p.first_name as first_name, p.last_name as last_name"
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print('  ', record['first_name'], record['last_name'])

        log.info("Step 3: Add colors to database")
        for hue in [('Red'), ('Orange'), ('Yellow')]:
            cyph = "CREATE (n:Color {hue: '%s'})" % (hue)
            session.run(cyph)

        log.info("Step 3a: Check colors in the DB")
        cyph = "MATCH (c:Color) RETURN c.hue as hue"
        result = session.run(cyph)
        print("Colors in database:")
        for record in result:
            print('  ', record['hue'])

        log.info("Step 4: Associate colors with people")
        log.info("Some people like red")
        for first, last in [('Leonardo', 'Davinci'),
                            ('Ansel', 'Adams'),
                            ]:
            cyph = """
                   MATCH (p:Person {first_name:'%s', last_name:'%s'}), (c:Color {hue: 'Red'})
                   CREATE (p)-[:LIKES]->(c)
                   """ % (first, last)
            session.run(cyph)
        log.info("Some people like orange")
        for first, last in [('Bob', 'Jones'),
                            ]:
            cyph = """
                   MATCH (p:Person {first_name:'%s', last_name:'%s'}), (c:Color {hue: 'Orange'})
                   CREATE (p)-[:LIKES]->(c)
                   """ % (first, last)
            session.run(cyph)
        log.info("Everyone likes yellow")
        for first, last in [('Bob', 'Jones'),
                            ('Marie', 'Curie'),
                            ('Leonardo', 'Davinci'),
                            ('Ansel', 'Adams'),
                            ]:
            cyph = """
                   MATCH (p:Person {first_name:'%s', last_name:'%s'}), (c:Color {hue: 'Yellow'})
                   CREATE (p)-[:LIKES]->(c)
                   """ % (first, last)
            session.run(cyph)

        log.info("Step 4a: Check likes")
        print("People who like Red:")
        cyph = "MATCH (:Color {hue: 'Red'})<-[:LIKES]-(p:Person) RETURN p"
        result = session.run(cyph)
        for record in result:
            for person in record.values():
                print('  ', person['first_name'], person['last_name'])
        print("People who like Orange:")
        cyph = "MATCH (:Color {hue: 'Orange'})<-[:LIKES]-(p:Person) RETURN p"
        result = session.run(cyph)
        for record in result:
            for person in record.values():
                print('  ', person['first_name'], person['last_name'])
        print("People who like Yellow:")
        cyph = "MATCH (:Color {hue: 'Yellow'})<-[:LIKES]-(p:Person) RETURN p"
        result = session.run(cyph)
        for record in result:
            for person in record.values():
                print('  ', person['first_name'], person['last_name'])

        log.info("Step 5: Everyone's favorite colors")
        name_cyph = "MATCH (p:Person) RETURN p.first_name as first_name, p.last_name as last_name"
        name_list = session.run(name_cyph)
        for name in name_list:
            print(f"{name['first_name']} {name['last_name']}'s favorite colors:")
            color_cyph = """
                         MATCH (:Person {first_name: '%s', last_name: '%s'})
                         -[:LIKES]->(c:Color) RETURN c.hue as hue
                         """ % (name['first_name'], name['last_name'])
            color_list = session.run(color_cyph)
            for color in color_list:
                print('  ', color['hue'])
