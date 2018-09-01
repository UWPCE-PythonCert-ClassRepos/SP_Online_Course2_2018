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
                            ('Woody', 'Allen'),
                            ('Woody', 'Harrelson'),
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

        log.info('Step 4: Create some colors')

        for color in [('Red'),
                      ('Orange'),
                      ('Yellow'),
                      ('Green'),
                      ('Blue'),
                      ('Indigo'),
                      ('Violet'),
                      ('Black'),
                     ]:
            cyph = "CREATE (n:Color {color:'%s'})" % (
                color)
            session.run(cyph)

        log.info("Step 5: Get all of colors in the DB:")

        cyph = """MATCH (c:Color)
                  RETURN c.color as color
                """

        result = session.run(cyph)

        print("Colors in database:")

        for record in result:
            print(record['color'])

        log.info('Step 6: Create some colors relationships')

        cypher = """
            MATCH (p:Person {first_name:'Woody', last_name:'Harrelson'})
            CREATE (p)-[fav:FAV]->(c:Color {color:'Red'})
            RETURN p
        """
        session.run(cypher)

        cypher = """
            MATCH (p:Person {first_name:'Woody', last_name:'Harrelson'})
            CREATE (p)-[fav:FAV]->(c:Color {color:'Blue'})
            RETURN p
        """
        session.run(cypher)

        cypher = """
            MATCH (p:Person {first_name:'Mary', last_name:'Evans'})
            CREATE (p)-[fav:FAV]->(c:Color {color:'Indigo'})
            RETURN p
        """
        session.run(cypher)

        cypher = """
            MATCH (p:Person {first_name:'Bob', last_name:'Jones'})
            CREATE (p)-[fav:FAV]->(c:Color {color:'Yellow'})
            RETURN p
        """
        session.run(cypher)

        cypher = """
            MATCH (p:Person {first_name:'Bob', last_name:'Jones'})
            CREATE (p)-[fav:FAV]->(c:Color {color:'Green'})
            RETURN p
        """
        session.run(cypher)

        log.info("Step 7: Find all of Woody Harrelson's colors")

        cyph = """
          MATCH (woody {first_name:'Woody', last_name:'Harrelson'})
                -[:FAV]->(woodyFavs)
          RETURN woodyFavs
          """

        result = session.run(cyph)

        print("Woody Harrelson's favorite colors are:")
        
        for rec in result:
            for color in rec.values():
                print(color['color'])

        log.info("Step 8: Find all of May Evans's colors")

        cyph = """
          MATCH (mary {first_name:'Mary', last_name:'Evans'})
                -[:FAV]->(maryFavs)
          RETURN maryFavs
          """

        result = session.run(cyph)

        print("Mary Evans's favorite colors are:")
        
        for rec in result:
            for color in rec.values():
                print(color['color'])

        log.info("Step 9: Find all of Bob Jones's colors")

        cyph = """
          MATCH (bob {first_name:'Bob', last_name:'Jones'})
                -[:FAV]->(bobFavs)
          RETURN bobFavs
          """

        result = session.run(cyph)

        print("Bob Jones's favorite colors are:")
        
        for rec in result:
            for color in rec.values():
                print(color['color'])

        log.info("Step 10: Print everyone's colors")

        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Woody', 'Allen'),
                            ('Woody', 'Harrelson'),
                            ]:

            cyph = """
            MATCH (person {first_name:'%s', last_name:'%s'})
                    -[:FAV]->(personFavs)
            RETURN personFavs
            """ % (first, last)

            result = session.run(cyph)

            print("{} {}'s favorite colors are:".format(first, last))
            
            for rec in result:
                for color in rec.values():
                    print(color['color'])
        
