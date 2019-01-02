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
                            ('Marie', 'Curie')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)
            
        log.info("Step 2b: Add more people")
        for first, last in [('Jimmy', 'Dean'),
                            ('James', 'Bond'),
                            ('JK', 'Rowling'),
                            ('Judy', 'Blume')
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

        # log.info('Step 4: Create some relationships')
        # log.info("Bob Jones likes Alice Cooper, Fred Barnes and Marie Curie")

        # for first, last in [("Alice", "Cooper"),
                            # ("Fred", "Barnes"),
                            # ("Marie", "Curie")]:
            # cypher = """
              # MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
              # CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              # RETURN p1
            # """ % (first, last)
            # session.run(cypher)

        # log.info("Step 5: Find all of Bob's friends")
        # cyph = """
          # MATCH (bob {first_name:'Bob', last_name:'Jones'})
                # -[:FRIEND]->(bobFriends)
          # RETURN bobFriends
          # """
        # result = session.run(cyph)
        # print("Bob's friends are:")
        # for rec in result:
            # for friend in rec.values():
                # print(friend['first_name'], friend['last_name'])

        # log.info("Setting up Marie's friends")

        # for first, last in [("Mary", "Evans"),
                            # ("Alice", "Cooper"),
                            # ('Fred', 'Barnes'),
                            # ]:
            # cypher = """
              # MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
              # CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
              # RETURN p1
            # """ % (first, last)

            # session.run(cypher)

        # print("Step 6: Find all of Marie's friends?")
        # cyph = """
          # MATCH (marie {first_name:'Marie', last_name:'Curie'})
                # -[:FRIEND]->(friends)
          # RETURN friends
          # """
        # result = session.run(cyph)
        # print("\nMarie's friends are:")
        # for rec in result:
            # for friend in rec.values():
                # print(friend['first_name'], friend['last_name'])

        log.info("Step 7: Add colors")
        for color in ['Red', 
                      'Orange', 
                      'Yellow', 
                      'Green',
                      'Indigo',
                      'Violet',
                      'Black',
                      'Brown'
                  ]:
            cyph = "CREATE (n:Color {color: '%s'})" % (color)
            session.run(cyph)
        
        log.info("Step 8: Get all of colors in the DB:")
        cyph = """MATCH (c:Color)
                  RETURN c.color as color
                """
        result = session.run(cyph)
        print("Colors in database:")
        for record in result:
            print(record['color'])
        
        log.info("Step 9: Add Favorite Colors")
        for fn, ln, fc in [('Bob', 'Jones', 'Red'),
                        ('Nancy', 'Cooper', 'Violet'),
                        ('Alice', 'Cooper','Black'),
                        ('Fred', 'Barnes', 'Green'),
                        ('Mary', 'Evans', 'Violet'),
                        ('Marie', 'Curie', 'Blue'),
                        ('Jimmy', 'Dean', 'Brown'),
                        ('James', 'Bond', 'Black'),
                        ('JK', 'Rowling', 'Red'),
                        ('Judy', 'Blume', 'Blue')
                        ]:
            cypher = """MATCH (p:Person {first_name: '%s', last_name: '%s'})
                        CREATE (p)-[f:FAVE_COLOR]->(c:Color {color: '%s'})
                        RETURN p, f, c""" % (fn, ln, fc)
                     
            session.run(cypher)
        
        log.info("Step 10: List Names and Colors")
        cyph = """MATCH (p:Person)-[f:FAVE_COLOR]->(c:Color)
                  RETURN p.first_name as first_name, p.last_name as last_name, c.color as color
               """
        result = session.run(cyph)
        for record in result:
            print(record['first_name'], record['last_name'], record['color'])
        
        log.info("Step 11: List Names by Favorite Color")
        colors = ['Red', 
                 'Orange', 
                 'Yellow', 
                 'Green',
                 'Indigo',
                 'Violet',
                 'Black',
                 'Brown'
                 ]
        for color_name in colors:
            print(color_name)
            namecyph = """MATCH (c:Color)<-[f:FAVE_COLOR]-(p:Person) WHERE (c.color = '%s')
                          RETURN c.color as color, p. first_name as first_name
                       """ % (color_name)
            nameresult = session.run(namecyph)
            for entry in nameresult:
                print(entry['first_name'])
            
        