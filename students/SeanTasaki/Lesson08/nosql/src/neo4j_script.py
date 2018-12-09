'''
Sean Tasaki
11/27/2018
Lesson08
'''

"""
    neo4j example
"""


import utilities
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def run_example():
    '''
    example of neo4j
    '''

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

        new_person = "CREATE (rummy:Person {first_name:'Sean', last_name:'Gaslight'}) RETURN rummy"
        session.run(new_person)
        new_person = "CREATE (rummy:Person {first_name:'Olive', last_name:'Dog'}) RETURN rummy"
        session.run(new_person)
        cypher = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cypher)

        log.info("Step 3: Get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])

        log.info('\n\nAdd colors')
        for color in ['black', 'blue', 'forest green', 'red', 'turquoise', 'rasberry' ]:
            cyphery = "CREATE (c:Color {color:'%s'})" % (color)
            session.run(cyphery)
        result1 = session.run(cyphery)
        print("\nColors in database:")
        for c in result1:
            print(c['color'])

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
        cypher = """MATCH (p:Person {first_name:'Sean'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'forest green'})
                RETURN p, f, c
                """
        session.run(cypher)

        cypher = """MATCH (p:Person {first_name:'Mary'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'forest green'})
                RETURN p, f, c
                """
        session.run(cypher)

        cypher = """MATCH (p:Person {first_name:'Bob'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'turquoise'})
                RETURN p, f, c
                """
        session.run(cypher)

        cypher = """MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person)
                RETURN c.color, p.first_name
                """
        result = session.run(cypher)
        for item in result:
            print(item.values()[0], "is a favorite color of", item.values()[1])

        log.info('\n\nFind who\'s favorite color is forest green')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='forest green') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for item in result:
            print(item.values()[1])
            
        log.info('\n\nFind who\'s favorite color is turquoise')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='turquoise') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for item in result:
            print(item.values()[1])

        log.info('\n\nWho likes what colors')
        query = """MATCH (c:Color)<-[:FAV_COLOR]-(p:Person) 
            RETURN c.color AS Color, collect(p.last_name) AS Last_Name"""
        results = session.run(query)
        for item in results:
            print(item.values()[0], "is a favorite color of", item.values()[1])


        log.info("Step 5: Find all of Bob's friends")
        cyph = """
          MATCH (bob {first_name:'Bob', last_name:'Jones'})
                -[:FRIEND]->(bobFriends)
          RETURN bobFriends
          """
        result = session.run(cyph)
        print("Bob's friends are:")
        for item in result:
            for friend in item.values():
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
