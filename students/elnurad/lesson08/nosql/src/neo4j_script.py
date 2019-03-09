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
                            ('Kelly', 'Moffett'),
                            ('Lena', 'Jensen'),
                            ('Carrie', 'Bradshow'),
                            ('Mike', 'Bird')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % ( #creating reusable node
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
        
        log.info('Adding a few color nodes')
        log.info('The cyph language is analagous to sql for neo4j')
        for color in ['red', 'blue', 'yellow', 'green', 'violet', 'brown', 'emerald', 'peach']:
            cyph = "CREATE (n:Color {color:'%s'})" % (color)
            session.run(cyph)

        log.info("Step 1: Get all colors in the DB:")
        cypher = """MATCH (c:Color)
                  RETURN c.color as color
                """
        result_color = session.run(cypher)
        print("Colors in database:")
        for record_color in result_color:
            print(record_color['color'])


        log.info('Step 2: Creating relationships between people and colors')
        log.info("Creating favorite colors for different persons in DB")
        for color in ['red', 'blue', 'yellow']:
            cypher = """
                MATCH (p:Person {first_name:'Bob', last_name:'Jones'})
                CREATE(p) - [f:FAVORITE_COLOR]->(c:Color {color: '%s'})
                RETURN p
                """ % (color)
            session.run(cypher)

        for color in ['violet', 'red', 'green']:
            cypher = """
                     MATCH (p:Person {first_name: 'Kelly', last_name: 'Moffett'})
                     CREATE(p) - [f:FAVORITE_COLOR]->(c:Color {color: '%s'})
                     RETURN p
                     """ % (color)
            session.run(cypher)
            
        for color in ['brown', 'emerald', 'peach']:
            cypher = """
                     MATCH (p:Person {first_name: 'Mike', last_name: 'Bird'})
                     CREATE(p) - [f:FAVORITE_COLOR]->(c:Color {color: '%s'})
                     RETURN p
                     """ % (color)
            session.run(cypher)

        log.info("Printing all of Bob's favorite colors")
        cyph = """
               MATCH(Bob {first_name: 'Bob', last_name: 'Jones'})-[:FAVORITE_COLOR]->(favorite_colors)
               RETURN favorite_colors
               """
        result = session.run(cyph)
        print("\nBob's favorite colors are:")
        for c in result:
            for val in c.values():
                print(val["color"])
        
        log.info("Printing Kelly's favorite colors")
        cyph = """
               MATCH(Kelly {first_name: 'Kelly', last_name: 'Moffett'})-[:FAVORITE_COLOR]->(favorite_colors)
               RETURN favorite_colors
               """
        result = session.run(cyph)
        print("\nKelly's favorite colors are:")
        for c in result:
            for val in c.values():
                print(val["color"])
         
        log.info("Step 3: Printing all of Mike's favorite colors")
        cyph = """
               MATCH(Mike {first_name: 'Mike', last_name: 'Bird'})-[:FAVORITE_COLOR]->(favorite_colors)
               RETURN favorite_colors
               """
        result = session.run(cyph)
        print("\nMike's favorite colors are:")
        for c in result:
            for val in c.values():
                print(val["color"])   
