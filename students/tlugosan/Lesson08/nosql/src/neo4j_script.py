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
                            ('Bob', 'Dylan'),
                            ('Albert', 'Einstein'),
                            ('Robert', 'DeVito'),
                            ('Brad', 'Pitt')
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

        log.info("Step 4.1: Create colors")
        colors = ['red', 'white', 'blue', 'green', 'yellow', 'purple']
        for color in colors:
            cyph = "CREATE (n:Color {color:'%s'})" % color
            session.run(cyph)

        log.info("Step 4.2: Get all the colors in DB:")
        cyph = """MATCH (c:Color)
                  RETURN c.color as color
                """
        result = session.run(cyph)
        print("Step 4.3: Colors in database:")
        for record in result:
            print(record['color'])

        log.info('Step 4.4: Create some color relashionships: ')
        log.info("Bob Jones, Nancy Cooper and Alice Cooper like white, "
                 "red and purple ")
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper')]:
            for color in ['red', 'white', 'purple']:
                cypher1 = """
                    MATCH(p1:Person), (c1:Color)
                    WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color='%s'
                    CREATE UNIQUE (p1)-[favorite:FAVORITE_COLOR]->(c1)
                    RETURN p1, favorite, c1
                    """ % (first, last, color)
                session.run(cypher1)

        log.info('Step 4.5: Create some color relashionships: ')
        log.info("Fred Barnes, Mary Evan, Marie Curie, Bob Dylan likes yellow,"
                 "green and purple")
        for first, last in [('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Bob', 'Dylan')]:
            for color in ['yellow', 'green', 'purple']:
                cypher2 = """
                    MATCH(p1:Person), (c1:Color)
                    WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color='%s'
                    CREATE UNIQUE(p1)-[favorite:FAVORITE_COLOR]->(c1)
                    RETURN p1, favorite, c1
                    """ % (first, last, color)
                session.run(cypher2)

        log.info('Step 4.6: Create some color relashionships: ')
        log.info("Fred Barnes, Mary Evan, Marie Curie, Bob Dylan likes yellow,"
                 "green and purple")
        log.info("Bob Dylan was added again for this set to demonstrate "
                 "uniqueness")
        for first, last in [('Bob', 'Dylan'),
                            ('Albert', 'Einstein'),
                            ('Robert', 'DeVito'),
                            ('Brad', 'Pitt')]:
            for color in ['blue', 'yellow']:
                cypher4 = """
                    MATCH(p1:Person), (c1:Color)
                    WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color='%s'
                    CREATE UNIQUE(p1)-[favorite:FAVORITE_COLOR]->(c1)
                    RETURN p1, favorite, c1
                    """ % (first, last, color)
                session.run(cypher4)

        log.info("Step 4.7: List each person and their colors")
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Bob', 'Dylan'),
                            ('Albert', 'Einstein'),
                            ('Robert', 'DeVito'),
                            ('Brad', 'Pitt')
                            ]:
            cypher6 = """
           MATCH (p1:Person{first_name:'%s', last_name:'%s'})-
           [:FAVORITE_COLOR]->(favorite_color)
           RETURN favorite_color
           """ % (first, last)
            result = session.run(cypher6)
            for rec in result:
                for res in rec.values():
                    print(first, last, res['color'])

        for color in colors:
            cypher7 = """
           MATCH (c1:Color{color:'%s'})<-
           [:FAVORITE_COLOR]-(p1:Person)
           RETURN p1.first_name as first_name, p1.last_name as last_name
           """ % color
            result7 = session.run(cypher7)
            for rec in result7:
                print(color + ": is a favorite of " + rec['first_name'] + " " +
                      rec['last_name'])

        # log.info('Step 4: Create some relationships')
        # log.info("Bob Jones likes Alice Cooper, Fred Barnes and Marie Curie")
        #
        # for first, last in [("Alice", "Cooper"),
        #                     ("Fred", "Barnes"),
        #                     ("Marie", "Curie")]:
        #     cypher = """
        #       MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
        #       CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
        #       RETURN p1
        #     """ % (first, last)
        #     session.run(cypher)
        #
        # log.info("Step 5: Find all of Bob's friends")
        # cyph = """
        #   MATCH (bob {first_name:'Bob', last_name:'Jones'})
        #         -[:FRIEND]->(bobFriends)
        #   RETURN bobFriends
        #   """
        # result = session.run(cyph)
        # print("Bob's friends are:")
        # for rec in result:
        #     for friend in rec.values():
        #         print(friend['first_name'], friend['last_name'])
        #
        # log.info("Setting up Marie's friends")
        #
        # for first, last in [("Mary", "Evans"),
        #                     ("Alice", "Cooper"),
        #                     ('Fred', 'Barnes'),
        #                     ]:
        #     cypher = """
        #       MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
        #       CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
        #       RETURN p1
        #     """ % (first, last)
        #
        #     session.run(cypher)
        #
        # print("Step 6: Find all of Marie's friends?")
        # cyph = """
        #   MATCH (marie {first_name:'Marie', last_name:'Curie'})
        #         -[:FRIEND]->(friends)
        #   RETURN friends
        #   """
        # result = session.run(cyph)
        # print("\nMarie's friends are:")
        # for rec in result:
        #     for friend in rec.values():
        #         print(friend['first_name'], friend['last_name'])
