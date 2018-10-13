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
            cypher = "MATCH (p1:Person {first_name:'Bob', last_name:'Jones'}), "
            cypher += f"(p2:Person {{first_name:'{first}', last_name:'{last}'}}) "
            cypher += "CREATE (p1)-[friend:FRIEND]->(p2) "
            cypher += "RETURN p1"
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
            cypher = "MATCH (p1:Person {first_name:'Marie', last_name:'Curie'}), "
            cypher += f"(p2:Person {{first_name:'{first}', last_name:'{last}'}}) "
            cypher += "CREATE (p1)-[friend:FRIEND]->(p2) "
            cypher += "RETURN p1"
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

        log.info('Step 7: Add a few more folks to the database')
        for first, last in [('Cary', 'Grant'),
                            ('James', 'Stewart'),
                            ('Audrey', 'Hepburn')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info("Step 8: Add some color")
        color_list = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        for color in color_list:
            cyph = "CREATE (c:color {name: '%s'})" % (
                color)
            session.run(cyph)

        log.info("Step 9: Make some favorite colors")
        fav_colors = dict()
        fav_colors[('Bob', 'Jones')] = ['red']
        fav_colors[('Nancy', 'Cooper')] = ['orange']
        fav_colors[('Alice', 'Cooper')] = ['yellow']
        fav_colors[('Fred', 'Barnes')] = ['green']
        fav_colors[('Mary', 'Evans')] = ['blue']
        fav_colors[('Marie', 'Curie')] = ['indigo']
        fav_colors[('Cary', 'Grant')] = ['red', 'violet']
        fav_colors[('James', 'Stewart')] = ['red', 'blue']
        fav_colors[('Audrey', 'Hepburn')] = ['red', 'orange']

        for name, colors in fav_colors.items():
            for color in colors:
                cypher = f"MATCH (p:Person {{first_name:'{name[0]}', last_name:'{name[1]}'}}), (c:color {{name:'{color}'}})"
                cypher += "CREATE (p)-[f:FAVORITE]->(c)"
                session.run(cypher)

        log.info("Step 10: List all the colors, and who has it as their favorite")
        for c in color_list:
            cyph = f"MATCH (person)-[:FAVORITE]->(c:color {{name: '{c}'}})"
            cyph += "RETURN person"
            result = session.run(cyph)

            log.info(f"People who have {c} as their favorite color:")
            for record in result:
                for person in record:
                    print(f"   {person['first_name']} {person['last_name']}")

        log.info("Step 11: List everyone, and their favorite colors")
        cyph = "MATCH (person)-[:FAVORITE]->(col)"
        cyph += "RETURN person.first_name as first_name, person.last_name as last_name, col.name as color_name"
        result = session.run(cyph)

        for record in result:
            print("The favorite color of",
                record['first_name'], record['last_name'],
                "is",
                record['color_name'])
