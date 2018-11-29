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

        ################################################################
        # Assignment
        ################################################################
        log.info("Step 7: Adding some new people and colors")
        new_person = "CREATE (p:Person {first_name:'Abdul', last_name:'Habibi'}) RETURN p"
        session.run(new_person)
        new_person = "CREATE (p:Person {first_name:'Yian', last_name:'Tsy'}) RETURN p"
        session.run(new_person)
        new_person = "CREATE (p:Person {first_name:'Ivan', last_name:'Smirnof'}) RETURN p"
        session.run(new_person)
        new_person = "CREATE (p:Person {first_name:'Steve', last_name:'Brendon'}) RETURN p"
        session.run(new_person)
        log.info("Step 7.1: AList all persons added (all distinc Person nodes)")
        cypher = """MATCH (p:Person)
                    RETURN p.first_name as first_name, p.last_name as last_name
                    ORDER BY last_name
                """
        # mind, using set in order to print out distinct Person nodes. Otherwise will print the same nodes as many time as 
        # associations it is defined with
        cursor = session.run(cypher)
        for i in sorted(set(cursor), key=lambda name: name[1]):
            print(i['first_name'], i['last_name'])
        
        log.info("Step 7.2: Creating colors")
        for color in ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'white', 'black', 'brown' ]:
            cyphery = "CREATE (c:Color {color:'%s'})" % (color)
            session.run(cyphery)
        
        cypher = """MATCH (c:Color)
                    RETURN c.color as color
                    ORDER BY color
                """
        cursor = session.run(cypher)
        print("Created colors:")
        # colors are not associated so far, no need using set
        for i in cursor:
            print(i['color'])
        
        log.info("Step 8: Creating associations between people and their favorite colors")
        cypher = """MATCH (p:Person {first_name:'Fred', last_name:'Barnes'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'blue'})
                RETURN p, f, c
                """
        session.run(cypher)
        cypher = """MATCH (p:Person {first_name:'Alice', last_name:'Cooper'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'green'})
                RETURN p, f, c
                """
        session.run(cypher)
        cypher = """MATCH (p:Person {first_name:'Nancy', last_name:'Cooper'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'brown'})
                RETURN p, f, c
                """
        session.run(cypher)
        cypher = """MATCH (p:Person {first_name:'Mary', last_name:'Evans'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'red'})
                RETURN p, f, c
                """
        session.run(cypher)
        cypher = """MATCH (p:Person {first_name:'Abdul', last_name:'Habibi'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'yellow'})
                RETURN p, f, c
                """
        session.run(cypher)
        cypher = """MATCH (p:Person {first_name:'Bob', last_name:'Jones'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'green'})
                RETURN p, f, c
                """
        session.run(cypher)
        cypher = """MATCH (p:Person {first_name:'Ivan', last_name:'Smirnof'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'red'})
                RETURN p, f, c
                """
        session.run(cypher)
        cypher = """MATCH (p:Person {first_name:'Yian', last_name:'Tsy'})  
                CREATE (p)-[f:FAV_COLOR]->(c:Color {color:'orange'})
                RETURN p, f, c
                """
        session.run(cypher)
        
        log.info("Step 9: Listing people having favorite color:")
        cypher = """
                    MATCH (p:Person)-[f:FAV_COLOR]->(c:Color)
                    RETURN p.first_name as first, p.last_name as last
                    ORDER BY last
                """
        cursor = session.run(cypher)
        for i in sorted(set(cursor), key=lambda name: name[1]):
            print("{:<10} {:<10}".format(i['first'], i['last']))

        log.info("Step 10: Listing people, who does not have favorite color:")
        cypher = """
                    MATCH (p:Person)
                    WHERE not (p:Person) -[:FAV_COLOR]->(:Color)
                    RETURN p.first_name as first, p.last_name as last
                    ORDER BY last
                """
        cursor = session.run(cypher)
        for i in sorted(set(cursor), key=lambda name: name[1]):
            print("{:<10} {:<10}".format(i['first'], i['last']))

        log.info("Step 11: Listing peoples favorit colors:")
        cypher = """
                    MATCH (c:Color)<-[f:FAV_COLOR]-(p:Person)
                    RETURN DISTINCT c.color as color, p.first_name as first, p.last_name as last
                    ORDER BY color
                """
        cursor = session.run(cypher)
        for i in cursor.values():
            print("Color: {}, First: {}, Last: {}".format(i[0], i[1], i[2]))