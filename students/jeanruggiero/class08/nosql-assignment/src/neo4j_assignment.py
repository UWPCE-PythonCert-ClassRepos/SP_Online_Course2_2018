"""
    neo4j example
"""


import utilities
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/neo4j_assignment.log')


def add_people():

    people = [
        ('Bob', 'Jones'),
        ('Nancy', 'Cooper'),
        ('Alice', 'Cooper'),
        ('Fred', 'Barnes'),
        ('Mary', 'Evans'),
        ('Marie', 'Curie'),
        ('Sally', 'Ride'),
        ('John', 'Glenn'),
        ('Neil', 'Armstrong')]

    colors = ['red', 'blue', 'green', 'orange', 'yellow']

    log.info('Step 1: First, clear the entire database, so we can start over')
    log.info("Running clear_all")

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add a few people and colors.")

    with driver.session() as session:

        log.info('Adding a few Person nodes')
        log.info('The cyph language is analagous to sql for neo4j')
        for first, last in people:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info('Adding a few Color nodes')
        for color in colors:
            cyph = "CREATE (n:Color {color: '%s'})" % (color)
            session.run(cyph)

        log.info("Step 3: Get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])

        log.info('Step 4: Create some favorite color relationships.')
        log.info("Bob Jones likes red, orange, and yellow")
        for color in ['red', 'orange', 'yellow']:
            cyph = """
                MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
                CREATE (p1)-[favorite_color:FAVORITE_COLOR]->(c1:Color {color:'%s'})
                RETURN p1
                """ % color
            session.run(cyph)

        log.info("Sally likes green.")
        cyph = """
            MATCH (p1:Person {first_name:'Sally', last_name:'Ride'})
            CREATE (p1)-[favorite_color:FAVORITE_COLOR]->(c1:Color {color:'green'})
            RETURN p1
            """
        session.run(cyph)

        log.info("Neil likes blue.")
        cyph = """
            MATCH (p1:Person {first_name:'Neil', last_name:'Armstrong'})
            CREATE (p1)-[favorite_color:FAVORITE_COLOR]->(c1:Color {color:'blue'})
            RETURN p1
            """
        session.run(cyph)

        log.info("Alice likes blue.")
        cyph = """
            MATCH (p1:Person {first_name:'Alice', last_name:'Cooper'})
            CREATE (p1)-[favorite_color:FAVORITE_COLOR]->(c1:Color {color:'blue'})
            RETURN p1
            """
        session.run(cyph)

        log.info('Step 5: print the people who have each color as their favorite.')
        for color in colors:
            cyph = """
                MATCH(c1 {color:'%s'})
                    -[:FAVORITE_COLOR]-(people)
                RETURN people
                """ % color
            result = session.run(cyph)
            print(f'People whose favorite color is {color}:')
            for rec in result:
                for person in rec.values():
                    print(person['first_name'], person['last_name'])

        log.info("Step 6: Print each person's favorite color(s).")
        for first, last in people:
            cyph = """
                MATCH(p1 {first_name:'%s', last_name:'%s'})
                    -[:FAVORITE_COLOR]->(colors)
                RETURN colors""" % (first, last)
            result = session.run(cyph)
            print(f"{first}'s favorite color(s):")
            for rec in result:
                for color in rec.values():
                    print(color['color'])
