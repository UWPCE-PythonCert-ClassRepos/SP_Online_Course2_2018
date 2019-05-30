"""
    neo4j example. Modified for Lesson 8 Part 1. Zach and Brian added
    to the database.
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

        log.info('Adding a few Person nodes, including Zach and Brian')
        log.info('The cyph language is analagous to sql for neo4j')
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Zach', 'Gillis'),
                            ('Brian', 'Fitztony')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info('Adding some colors to the database.')

        for colors in ['Red', 'Blue', 'Green', 'Orange', 'Pink']:
            cyph = "CREATE (c:Color {color:'%s'})" % colors
            session.run(cyph)

        log.info("Get all the colors in the DB:")
        cyph = """MATCH (c:Color)
                  RETURN c.color as color
                """
        result = session.run(cyph)
        print("Colors in database:")
        for color in result:
            print(color['color'])

        log.info("Create Relationships between people and color:")
        log.info("Zach's favorite color is pink:")
        cyph = """
                    MATCH (p1:Person {first_name: 'Zach'}),(c1:Color {color:'Pink'})
                    CREATE (p1)-[:FAVORITE_COLOR_IS]->(c1)
                    """
        session.run(cyph)

        log.info("Zach has two favorite colors, the other is red.")
        cyph = """
                    MATCH (p1:Person {first_name: 'Zach'}),(c1:Color {color:'Red'})
                    CREATE (p1)-[:FAVORITE_COLOR_IS]->(c1)
                    """
        session.run(cyph)

        log.info("Bob's favorite color is red:")
        cyph = """
                    MATCH (p1:Person {first_name: 'Bob'}),(c1:Color {color:'Red'})
                    CREATE (p1)-[:FAVORITE_COLOR_IS]->(c1)
                    """
        session.run(cyph)

        log.info("Nancy's favorite color is blue:")
        cyph = """
                    MATCH (p1:Person {first_name: 'Nancy'}),(c1:Color {color:'Blue'})
                    CREATE (p1)-[:FAVORITE_COLOR_IS]->(c1)
                    """
        session.run(cyph)

        log.info("Mary's favorite color is blue:")
        cyph = """
                    MATCH (p1:Person {first_name: 'Mary'}),(c1:Color {color:'Blue'})
                    CREATE (p1)-[:FAVORITE_COLOR_IS]->(c1)
                    """
        session.run(cyph)

        log.info("Alice's favorite color is green:")
        cyph = """
                    MATCH (p1:Person {first_name: 'Alice'}),(c1:Color {color:'Green'})
                    CREATE (p1)-[:FAVORITE_COLOR_IS]->(c1)
                    """
        session.run(cyph)

        log.info("Fred's favorite color is orange:")
        cyph = """
                    MATCH (p1:Person {first_name: 'Fred'}),(c1:Color {color:'Orange'})
                    CREATE (p1)-[:FAVORITE_COLOR_IS]->(c1)
                    """
        session.run(cyph)

        log.info("Executing a color query that lists all the people who have "
                 "this color as their favorite.")
        color_dict = {}  # dictionary with a color as the key, and a list
        # of names related to each color

        colors = ['Red', 'Blue', 'Green', 'Orange', 'Pink']
        for color in colors:
            names = []  # list to hold names associated with a color
            cyph = """
                    MATCH (p:Person)--(c: Color {color: '%s'})
                    RETURN p.first_name as first_name
                    """ % color

            color_results = session.run(cyph)

            for result in color_results:
                names.append(result["first_name"])

            color_dict[color] = names

        for key, values in color_dict.items():
            print(f'These people,{values} have a favorite color of {key}.')

        log.info("Can you also list all of everyone's favorite colors?")
        log.info("Query to find everyone with a favorite color, then list color"
                 "associated with that person.")
        log.info("This is similar to the above query, but now a person may have"
                 "more than one favorite color. So instead of searching by color"
                 "we search by relationship.")

        log.info("First, we will get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name
                """
        result = session.run(cyph)
        log.info("People in database are put in a list and we search for"
                 "all colors that are related to their name.")
        name_list = []
        for record in result:
            name_list.append(record['first_name'])

        # search over all people in database for
        # any relationship [:Favorite_color_is]

        for name in name_list:
            cyph = """
                MATCH (p:Person {first_name:'%s'})-[:FAVORITE_COLOR_IS]->(c)
                RETURN c.color as color
                """ % name

            color_results = session.run(cyph)
            for result in color_results:
                print(f'{name} has favorite color {result["color"]}')















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
