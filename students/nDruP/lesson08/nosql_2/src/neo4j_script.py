"""
    neo4j example
"""


import utilities
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def run_example():
    input('Neo4j example. Press enter to continue.........')
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
                            ('Fred', 'Barnes')]:
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

        log.info('Assignment: Add some new people to the database.')
        new_people = [("Andrew", "Park"),
                      ("Sleve", "McDichael"),
                      ("Beyonce", "Knowles")]
        for first, last in new_people:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
            first, last)
            session.run(cyph)
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])

        log.info('Then add some colors.')
        colors = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        colors += [x + ' ' + y for x in ['Light', 'Dark'] for y in colors]
        for color in colors:
            cyph = "CREATE (n: Color{color:'%s'})" % color
            session.run(cyph)
        cyph = """MATCH (c:Color)
        RETURN c.color as color
        """
        result = session.run(cyph)
        print("Colors in database:")
        for record in result:
            print(record['color'])        
        
        log.info('Create associations between people and '
                 'their favorite colors(they can have more than one).')
        drew_colors = [x for x in colors if colors.index(x) % 2 == 1]
        sleve_colors = [x for x in colors if colors.index(x) % 3 == 1]
        bey_colors = [x for x in colors if colors.index(x) % 3 == 2]
        for c in drew_colors:
            cypher = """
            MATCH (p1:Person {first_name:'Andrew', last_name:'Park'})
            CREATE (p1)-[favorite: COLOR]->(c:Color {color:'%s'})
            RETURN p1
            """ % (c)
            session.run(cypher)
        for c in sleve_colors:
            cypher = """
            MATCH (p1:Person {first_name:'Sleve', last_name:'McDichael'})
            CREATE (p1)-[favorite: COLOR]->(c:Color {color:'%s'})
            RETURN p1
            """ % (c)
            session.run(cypher)
        for c in bey_colors:
            cypher = """
            MATCH (p1:Person {first_name:'Beyonce', last_name:'Knowles'})
            CREATE (p1)-[favorite: COLOR]->(c:Color {color:'%s'})
            RETURN p1
            """ % (c)
            session.run(cypher)
        
        log.info('List all of the people who have each '
                 'color as their favorite.')
        for c in colors:
            cyph = """ MATCH(p:Person)-[favorite: COLOR]->(c:Color{color:'%s'})
            return c.color as color, p.first_name as first, p.last_name as last
            """ % (c)
            result = session.run(cyph)
            for record in result:
                print(record['color']+' is one of '+
                      record['first']+' '+record['last'] +"'s favorite colors") 
        
        log.info('Can you also list all of the everyones favorite colors?')
        for first, last in new_people:
            cyph = """ MATCH(p:Person{first_name:'%s', last_name:'%s'})
            -[favorite: COLOR]->(c:Color)
            return c.color as color, p.first_name as first, p.last_name as last
            """ % (first, last)
            result = session.run(cyph)
            for record in result:
                print('One of '+ record['first']+' '+record['last']+
                      "'s favorite colors is "+record['color']) 
            
