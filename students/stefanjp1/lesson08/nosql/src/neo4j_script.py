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
                            ('Stefan', 'Partin'),
                            ('Mason', 'Matlock'),
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

        log.info('** Add some colors')
        for color in ['blue', 'green', 'orange', 'yellow', 'red']:
            cyphery = "CREATE (c:Color {color:'%s'})" % (color)
            session.run(cyphery)   
        
        log.info("** Colors in the database")
        cyph = """MATCH (c:Color)
                  RETURN c.color as color
                """
        result = session.run(cyph)
        print("Colors in database:")
        for record in result:
            print(record['color'])
        
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
        
        log.info('** Create person favorite color relationships')
        cyph = """MATCH (p:Person {first_name:'Stefan', last_name:'Partin'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'blue'})
                RETURN p, f, c
                """
        session.run(cyph)
        
        cyph = """MATCH (p:Person {first_name:'Mason', last_name:'Matlock'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'green'})
                RETURN p, f, c
                """
        session.run(cyph)
        
        cyph = """MATCH (p:Person {first_name:'Mary', last_name:'Evans'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'green'})
                RETURN p, f, c
                """
        session.run(cyph)
        
        cyph = """MATCH (p:Person {first_name:'Alice', last_name:'Cooper'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'yellow'})
                RETURN p, f, c
                """
        session.run(cyph)
        
        cyph = """MATCH (p:Person {first_name: "Nancy", last_name:'Cooper'})   
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'red'})
                RETURN p, f, c
                """
        session.run(cyph)
        
        cyph = """MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person)
                RETURN c.color, p.first_name
                """
        result = session.run(cyph)
        for record in result:
            print(f"{record.values()[1]} favorite color is {record.values()[0]}")
        
        log.info('** People with favorite color blue:')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='blue') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for record in result:
            print(record.values()[1])
            
        log.info('** People with favorite color green:')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='green') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for record in result:
            print(record.values()[1])
            
        log.info('** People with favorite color red:')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='red') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for record in result:
            print(record.values()[1])
            
        log.info('** People with favorite color yellow:')
        q = """
            MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person) WHERE (c.color ='yellow') RETURN c.color, p.last_name
            """
        result = session.run(q)
        for record in result:
            print(record.values()[1]) 

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
