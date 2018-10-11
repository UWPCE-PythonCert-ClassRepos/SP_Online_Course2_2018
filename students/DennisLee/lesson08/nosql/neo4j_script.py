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
        people = [
            ('Bob', 'Jones'),
            ('Nancy', 'Cooper'),
            ('Alice', 'Cooper'),
            ('Fred', 'Barnes'),
            ('Mary', 'Evans'),
            ('Marie', 'Curie'),
        ]
        for first, last in people:
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

        log.info("Skipping steps 4 through 6 since the friend relationship "
                 "creations cause duplicate person/color relationships later.")

        # log.info('Step 4: Create some relationships')
        # log.info("Bob Jones likes Alice Cooper, Fred Barnes and Marie Curie")

        # for first, last in [("Alice", "Cooper"),
        #                     ("Fred", "Barnes"),
        #                     ("Marie", "Curie")]:
        #     cypher = """
        #       MATCH (p1:Person {first_name:'Bob', last_name:'Jones'})
        #       CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
        #       RETURN p1
        #     """ % (first, last)
        #     session.run(cypher)

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

        # log.info("Setting up Marie's friends")

        # for first, last in [("Mary", "Evans"),
        #                     ("Alice", "Cooper"),
        #                     ('Fred', 'Barnes'),
        #                    ]:
        #     cypher = """
        #       MATCH (p1:Person {first_name:'Marie', last_name:'Curie'})
        #       CREATE (p1)-[friend:FRIEND]->(p2:Person {first_name:'%s', last_name:'%s'})
        #       RETURN p1
        #     """ % (first, last)

        #     session.run(cypher)

        # log.info("Step 6: Find all of Marie's friends?")
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

        log.info("Step 7: Add more people")
        emcees = [
            ('Bob', 'Barker'),
            ('Tom', 'Kennedy'),
            ('Regis', 'Philbin'),
            ('Vicki', 'Lawrence')
        ]
        for first, last in emcees:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)
        people.extend(emcees)  # Add emcees to rest of people list
        people.sort(key=lambda x: (x[1], x[0]))  # Sort people by last name

        log.info("Step 8: Add colors")
        color_list = ['Red', 'White', 'Blue', 'Green',
                      'Purple', 'Orange', 'Yellow', 'Brown', 'Black']
        color_list.sort()
        for color in color_list:
            cyph = "CREATE (c:Color {color: '%s'})" % color
            session.run(cyph)

        log.info("Step 9: Set color likes")
        log.info("Set favorite color")
        for first, last, fav_color in [
                ('Bob', 'Jones', 'Brown'),
                ('Nancy', 'Cooper', 'Orange'),
                ('Alice', 'Cooper', 'Yellow'),
                ('Fred', 'Barnes', 'Blue'),
                ('Mary', 'Evans', 'Yellow'),
                ('Marie', 'Curie', 'White'),
                ('Bob', 'Barker', 'Purple'),
                ('Tom', 'Kennedy', 'Brown'),
                ('Regis', 'Philbin', 'Green'),
                ('Vicki', 'Lawrence', 'Red')
        ]:
            cypher = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[likes:LIKES]->(c:Color {color: '%s'})
              RETURN p
            """ % (first, last, fav_color)
            session.run(cypher)

        log.info("Set women to like blue")
        for first, last in [
                ('Nancy', 'Cooper'),
                ('Alice', 'Cooper'),
                ('Mary', 'Evans'),
                ('Marie', 'Curie'),
                ('Vicki', 'Lawrence')
        ]:
            cypher = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[likes:LIKES]->(c:Color {color: 'Blue'})
              RETURN p
            """ % (first, last)
            session.run(cypher)

        log.info("Set men to like black")
        for first, last in [
                ('Bob', 'Jones'),
                ('Fred', 'Barnes'),
                ('Bob', 'Barker'),
                ('Tom', 'Kennedy'),
                ('Regis', 'Philbin')
        ]:
            cypher = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[likes:LIKES]->(c:Color {color: 'Black'})
              RETURN p
            """ % (first, last)
            session.run(cypher)

        log.info("Set Bobs to like green")
        cypher = """
            MATCH (p:Person {first_name: 'Bob'})
            CREATE (p)-[likes:LIKES]->(c:Color {color: 'Green'})
            RETURN p
        """
        session.run(cypher)

        log.info("Set Coopers to like purple")
        cypher = """
            MATCH (p:Person {last_name: 'Cooper'})
            CREATE (p)-[likes:LIKES]->(Color {color: 'Purple'})
            RETURN p
        """
        session.run(cypher)

        log.info("Step 10: List all people who like a color")
        for color in color_list:
            cypher = """
                MATCH ((p)-[:LIKES]->(c:Color {color: '%s'}))
                RETURN p
                ORDER BY p.last_name, p.first_name
            """ % color

            result = session.run(cypher)
            print(f"\nPeople who like {color}: ")
            for person in result:
                for val in person.values():
                    print(f"\t{val['first_name']} {val['last_name']}")

        log.info("Step 11: List each person's color likes")
        for first, last in people:
            cypher = """
                MATCH ((p {first_name:'%s', last_name:'%s'})-[:LIKES]->(c))
                RETURN c
                ORDER BY c.color
            """ % (first, last)

            result = session.run(cypher)
            print(f"\n{first} {last}'s favorite colors: ")
            for color in result:
                for val in color.values():
                    print(f"\t{val['color']}")
