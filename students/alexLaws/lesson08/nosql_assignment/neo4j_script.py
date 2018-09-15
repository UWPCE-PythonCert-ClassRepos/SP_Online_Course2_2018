"""
    neo4j example
"""


import utilities
import login_database
import utilities

log = utilities.configure_logger('default', 'logs/neo4j_script.log')


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
                            ('Bill', 'Clinton'),
                            ('Hillary', 'Clinton'),
                            ('Barack', 'Obama'),
                            ('Michelle', 'Obama')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info("Step 3: Get all of people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        result_copy = []  # creating a copy to use later on
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])
            result_copy.append(record)

        for color in ['Grey',
                      'Pink',
                      'Orange',
                      'Yellow',
                      'Green',
                      'Blue',
                      'Red']:
            color_cyph = "CREATE (c:Color {color:'%s'})" % (color)
            session.run(color_cyph)

        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper')]:
            for color in ['Grey',
                          'Pink',
                          'Orange']:
                fav_color_cyph_1 = """MATCH (p1:Person), (c1:Color)
                                      WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color="%s"
                                      create (p1)-[f:FAVORITE_COLOR]->(c1)
                                      return p1, f, c1
                """ % (first, last, color)
                session.run(fav_color_cyph_1)

        for first, last in [('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Bill', 'Clinton'),
                            ('Hillary', 'Clinton')]:
            for color in ['Orange',
                          'Yellow',
                          'Green']:
                fav_color_cyph_2 = """MATCH (p1:Person), (c1:Color)
                                      WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color="%s"
                                      create (p1)-[f:FAVORITE_COLOR]->(c1)
                                      return p1, f, c1
                """ % (first, last, color)
                session.run(fav_color_cyph_2)

        for first, last in [('Barack', 'Obama'),
                            ('Michelle', 'Obama')]:
            for color in ['Yellow',
                          'Green',
                          'Blue',
                          'Red']:
                fav_color_cyph_3 = """MATCH (p1:Person), (c1:Color)
                                      WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color="%s"
                                      create (p1)-[f:FAVORITE_COLOR]->(c1)
                                      return p1, f, c1
                """ % (first, last, color)
                session.run(fav_color_cyph_3)

        all_color_cyph = """MATCH (c1:Color)
                            RETURN c1.color
        """
        all_colors = session.run(all_color_cyph)

        for fav_color in all_colors:
            who_likes_cyph = """MATCH (color_likers)-[f:FAVORITE_COLOR]->(c1 {color:'%s'})
                                RETURN color_likers
            """ % (fav_color)
            output = session.run(who_likes_cyph)
            favorite = fav_color.values()[0]
            print("The people who like {} are:".format(favorite))
            for row in output:
                for liker in row.values():
                    print(liker['first_name'], liker['last_name'])

        # recalling the result cypher from earlier that pulled all people

        for record in result_copy:
            first = record['first_name']
            last = record['last_name']
            likes_what_cyph = """MATCH (p1:Person)-[f:FAVORITE_COLOR]->(likes_what_colors)
                                 WHERE p1.first_name='%s' AND p1.last_name='%s'
                                 RETURN likes_what_colors
            """ % (first, last)
            print('{} {}\'s favorite colors are:'.format(first, last))
            color_output = session.run(likes_what_cyph)
            for row in color_output:
                print(row.values()[0]['color'])

        '''
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
        '''
