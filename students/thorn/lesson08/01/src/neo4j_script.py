"""
    neo4j example
"""


import utilities
import login_database
import utilities
import random

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
        people = [
            ('Bob', 'Jones'),
            ('Nancy', 'Cooper'),
            ('Marie', 'Curie'),
            ('Thomas', 'Horn'),
            ('Ted', 'H'),
            ('Bailey', 'K')
            ]

        for first, last in people:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info("Step 3: Get all of people and color:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
               """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])
     
        log.info("Step 4: Adding colors.")
        colors_list = ['blue', 'red', 'pink', 'orange', 'brown', 'black']
        for color in colors_list:
            cyph = "CREATE (c:Color {color:'%s'})" % (color)
            session.run(cyph)

        cyph = """MATCH (c:Color)
                  RETURN c.color as color
                 """
        result = session.run(cyph)
        print("Colors in database:")
        for record in result:
            print(record['color'])

        log.info("Step 5: Adding color relationships.")

        # for first, last in people:
        #     cyph = """
        #             MATCH (p1:Person {first_name:'%s', last_name:'%s'})
        #             CREATE (p1)-[f:fav_color]->(p2:Color {color:'%s'})
        #             RETURN p1
        #             """ % (first, last, color[random.randint(0, 4)])
        #     session.run(cyph)

        cyph = """
        MATCH (p:Person {first_name:'Thomas', last_name:'Horn'})
        CREATE (p)-[:fav_color]->(n:Color {color:'blue'})
        RETURN p
        """
        session.run(cyph)

        cyph = """
        MATCH (p:Person {first_name:'Nancy', last_name:'Cooper'})
        CREATE (p)-[:fav_color]->(n:Color {color:'red'})
        RETURN p
        """
        session.run(cyph)

        cyph = """
        MATCH (p:Person {first_name:'Ted', last_name:'H'})
        CREATE (p)-[:fav_color]->(n:Color {color:'pink'})
        RETURN p
        """
        session.run(cyph)

        for first, last in people:
            cyph = """
                   MATCH (person {first_name:'%s', last_name:'%s'})
                   -[:fav_color]->(per_color)
                   RETURN per_color
                   """ % (first, last)
            result = session.run(cyph)
            for record in result:
                for item in record.values():
                    if item:
                        print(f"{first} {last}'s favorite color is : {item['color']}")




