"""
Shin Tran
Python 220
Lesson 8 Assignment
Neo4j example
"""


import utilities
import login_database
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
        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Doug', 'Baldwin'),
                            ('Tyler', 'Lockett'),
                            ('Marshawn', 'Lynch')]:
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
        colors = ['Black','Blue','Green','Orange','Purple','Red','White','Yellow']

        for first, last in [('Bob', 'Jones'),
                            ('Nancy', 'Cooper'),
                            ('Alice', 'Cooper'),
                            ('Fred', 'Barnes'),
                            ('Mary', 'Evans'),
                            ('Marie', 'Curie'),
                            ('Doug', 'Baldwin'),
                            ('Tyler', 'Lockett'),
                            ('Marshawn', 'Lynch')]:
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
                            ('Doug', 'Baldwin'),
                            ('Tyler', 'Lockett'),
                            ('Marshawn', 'Lynch')]:
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


        log.info('Step 6: Print each color and the person that has the color as their favorite')
        for color in ['Black','Blue','Green','Orange','Purple','Red','White','Yellow']:
            cyph = """
              MATCH (c1:Color {name:'%s'})
              -[:Person]->(ppl)
              RETURN ppl
            """ % (color)
            result = session.run(cyph)
            for item in result:
                for names in item.values():
                    print(names)


if __name__ == '__main__':
    run_example()
