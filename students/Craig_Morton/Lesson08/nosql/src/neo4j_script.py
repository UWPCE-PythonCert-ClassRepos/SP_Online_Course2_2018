"""
Neo4j example
"""


import utilities
import login_database
import random

log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def run_example():

    log.info('Step 1: Clear the database')

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    log.info("Step 2: Add people to the database")

    with driver.session() as session:

        log.info('Adding people')
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Bill', 'Gates'),
                            ('Elon', 'Musk'),
                            ('Nikola', 'Tesla')]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info("Step 3: Get all people in database:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])

        log.info('Step 4: Create person and color relationship')
        colors = ['Black', 'Blue', 'Green', 'Orange', 'Purple', 'Red', 'White', 'Yellow']

        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Bill', 'Gates'),
                            ('Elon', 'Musk'),
                            ('Nikola', 'Tesla')]:
            cypher = """
              MATCH (p1:Person {first_name:'%s', last_name:'%s'})
              CREATE (p1)-[favcolor:FAVCOLOR]->(c1:Color {name:'%s'})
              RETURN p1
            """ % (first, last, colors[random.randint(0, 7)])
            session.run(cypher)

        log.info('Step 5: Print each person and their favorite color')
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Bill', 'Gates'),
                            ('Elon', 'Musk'),
                            ('Nikola', 'Tesla')]:
            cyph = """
              MATCH (p1:Person {first_name:'%s', last_name:'%s'})
              -[:FAVCOLOR]->(fav_color)
              RETURN fav_color
            """ % (first, last)
            result = session.run(cyph)
            for item in result:
                for clr in item.values():
                    if clr:
                        print("{} {}'s favorite color is: {}".format(first, last, clr['name']))

        log.info('Step 6: Print groups of people based on their favorite color')
        for color in ['Black', 'Blue', 'Green', 'Orange', 'Purple', 'Red', 'White', 'Yellow']:
            cyph = """ MATCH(c1:Color {name:'%s'})
            <-[favcolor:FAVCOLOR]
            -(p1:Person)
            return p1.first_name as first, p1.last_name as last
            """ % color
            result = session.run(cyph)
            print("Color " + color + " is the favorite color for: ")
            for record in result:
                print('    ' + record['first'] + ' ' + record['last'])


if __name__ == '__main__':
    run_example()
