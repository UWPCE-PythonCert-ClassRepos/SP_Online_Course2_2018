"""
    neo4j example
"""


import utilities
import login_database
import utilities

log = utilities.configure_logger('default', '../logs/neo4j_script.log')
driver = login_database.login_neo4j_cloud()


def clearDB():
    print('\nStep 1: First, clear the entire database, so we can start over')

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def populate_Person():

    print("\nStep 2: Add a few people")

    with driver.session() as session:

        log.info('Adding a few Person nodes')
        log.info('The cyph language is analagous to sql for neo4j')
        for first, last in [('Bob', 'Jones',),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Sally', 'Hill'),
                            ('Bob', 'Tomkins'),
                            ('David', 'Jackson'),
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        print("\nStep 3: Get all of people in the DB:")

        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:\n")
        for record in result:
            print(record['first_name'], record['last_name'])


def populate_Colors():
        print("\nStep 4: Adding some colors ")

        with driver.session() as session:

            for color in ['Blue',
                          'Orange',
                          'Green',
                          'Red',
                          'Maroon',
                          'Black',
                          'Purple',
                          'Gold',
                          'Yellow',
                          ]:
                cyph = "CREATE (n:Color {color:'%s'})" % (
                    color)
                session.run(cyph)

            color_cyph = """MATCH (c:Color)
                            RETURN c.color as color_name
                         """
            colors = session.run(color_cyph)

            print("Colors in database:\n")
            for row in colors:
                print(row['color_name'])


def create_bob_relationships():

    with driver.session() as session:

        print('\nStep 5: Create some relationships')
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

        print("\nStep 6: Find all of Bob's friends")

        cyph = """
          MATCH (bob {first_name:'Bob', last_name:'Jones'})
                -[:FRIEND]->(bobFriends)
          RETURN bobFriends
          """
        result = session.run(cyph)

        print("\nBob's friends are:\n")

        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])


def create_marie_relationships():

    with driver.session() as session:

        print("\nSetting up Marie's friends...")

        for first, last in [("Mary", "Evans"),
                            ("Alice", "Cooper"),
                            ('Fred', 'Barnes')
                            ]:
            cypher = """
                      MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
                      CREATE (p1)-[:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
                      RETURN p1
                    """ % (first, last)

            session.run(cypher)

        print("\nStep 7: Find all of Marie's friends?")

        mariecyph = """
                      MATCH (marie {first_name:'Marie', last_name:'Curie'})
                      -[f:FRIEND]->(marieFriends)
                      RETURN marieFriends
                    """
        result = session.run(mariecyph)

        print("\nMarie's friends are:\n")
        for rec in result:
            for friend in rec.values():
                print(friend['first_name'], friend['last_name'])


def create_color_rels():

    with driver.session() as session:

        print("\ncreating color relationships...")

        for first, last in [("Mary", "Evans"),
                            ("Alice", "Cooper"),
                            ('Fred', 'Barnes')
                            ]:
            for color in ['Blue',
                          'Orange',
                          'Green',
                          'Red']:

                cypher = """
                          MATCH (p1:Person), (c1:Color)
                          WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color='%s'
                          CREATE (p1)-[r:FAVCOLOR]->(c1)
                          RETURN p1, r, c1
                        """ % (first, last, color)

                session.run(cypher)

        for first, last in [('Bob', 'Jones',),
                            ('Nancy', 'Cooper'),
                            ('David', 'Jackson')
                            ]:
            for color in ['Maroon',
                          'Black',
                          'Purple']:

                cypher = """
                          MATCH (p1:Person), (c1:Color)
                          WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color='%s'
                          CREATE (p1)-[r:FAVCOLOR]->(c1)
                          RETURN p1, r, c1
                        """ % (first, last, color)

                session.run(cypher)

        for first, last in [('Marie', 'Curie'),
                            ('Sally', 'Hill'),
                            ('Bob', 'Tomkins'),
                            ('David', 'Jackson'),
                            ]:
            for color in ['Gold',
                          'Yellow']:

                cypher = """
                          MATCH (p1:Person), (c1:Color)
                          WHERE p1.first_name='%s' AND p1.last_name='%s' AND c1.color='%s'
                          CREATE (p1)-[r:FAVCOLOR]->(c1)
                          RETURN p1, r, c1
                        """ % (first, last, color)

                session.run(cypher)


def get_color_prefs_by_color():
    print("\n")
    log.info("Preferences by color")
    print("----------"*5)
    with driver.session() as session:
        for color in ['Blue',
                      'Orange',
                      'Green',
                      'Red',
                      'Maroon',
                      'Black',
                      'Purple',
                      'Gold',
                      'Yellow',
                      ]:

            fav_color = """
                          MATCH (all)-[r:FAVCOLOR]->(c1 {color:'%s'})
                          RETURN all
                        """ % (color)
            result = session.run(fav_color)

            print(f"\nPeople who like the color {color}:\n")
            for rec in result:
                for value in rec.values():
                    print(value['first_name'], value['last_name'])


def get_color_prefs_by_name():
    print("\n")
    log.info("Individual color preferences")
    print("----------"*5)
    with driver.session() as session:
        for first, last in [('Bob', 'Jones',),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Sally', 'Hill'),
                            ('Bob', 'Tomkins'),
                            ('David', 'Jackson'),
                            ]:

            fav_color = """
                          MATCH (all)<-[r:FAVCOLOR]-(p1 {first_name:'%s', last_name:'%s'})
                          RETURN all
                        """ % (first, last)
            result = session.run(fav_color)

            print(f"\n{first} {last} Likes:")

            for rec in result:
                for value in rec.values():
                    print(value['color'])


def run_example():
    clearDB()
    populate_Person()
    populate_Colors()
    create_color_rels()
    get_color_prefs_by_color()
    get_color_prefs_by_name()
    # create_bob_relationships()
    # create_marie_relationships()
