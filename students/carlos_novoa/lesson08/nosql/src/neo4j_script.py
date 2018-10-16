"""
    Neo4j
"""


import utilities
import login_database
log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def run_example():
    """
    Refactored Neo4j example
    """

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    with driver.session() as session:

        people = [('Bob', 'Jones'),
                  ('Nancy', 'Cooper'),
                  ('Alice', 'Cooper'),
                  ('Fred', 'Barnes'),
                  ('Mary', 'Evans'),
                  ('Marie', 'Curie'),
                  ('Jim', 'Halpert'),
                  ('Pam', 'Beesley'),
                  ('Dwigt', 'Chang')]

        favorites = [('Bob', 'Jones', 'Orange'),
                     ('Nancy', 'Cooper', 'Teal'),
                     ('Alice', 'Cooper', 'Black'),
                     ('Fred', 'Barnes', 'Teal'),
                     ('Mary', 'Evans', 'Blue'),
                     ('Marie', 'Curie', 'Blue'),
                     ('Marie', 'Curie', 'Teal'),
                     ('Jim', 'Halpert', 'Orange'),
                     ('Pam', 'Beesley', 'Green'),
                     ('Dwigt', 'Chang', 'Black'),
                     ('Dwigt', 'Chang', 'Green')]

        colors = ['Green', 'Orange', 'Teal', 'Black', 'Blue']

        log.info('Create person nodes')
        for first, last in people:
            cyph = "CREATE (p:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info('Create color nodes')
        for c in colors:
            cyph = "CREATE (:Color {color: '%s'})" % c
            session.run(cyph)

        log.info('Set associations between people and colors')
        for first, last, color in favorites:
            cypher = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[favorite:FAVORITE]->(:Color {color: '%s'})
              RETURN p
            """ % (first, last, color)
            session.run(cypher)

        log.info("Query by colors")
        for c in colors:
            cypher = """
                MATCH ((p)-[:FAVORITE]->(:Color {color: '%s'}))
                RETURN p
            """ % c

            result = session.run(cypher)
            print(f'\n\n{c}:')
            for properties in result:
                for p in properties:
                    print(f"  {p['first_name']} {p['last_name']}")
        print('\n\n')

        log.info("Query by person")
        print('\n')
        for first, last in people:
            cypher = """
                MATCH ((p {first_name:'%s', last_name:'%s'})-[:FAVORITE]->(c))
                RETURN c
            """ % (first, last)

            result = session.run(cypher)

            fc = []
            for properties in result:
                for p in properties:
                    fc.append(p['color'])

            print("{} {}'s favorites: {}".format(first, last, ', '.join(fc)))

        print('\n\n')
