"""
    people and colors assignment using neo4j
"""

import utilities
import login_database


log = utilities.configure_logger('default', '../logs/people_neo4j.log')
driver = login_database.login_neo4j_cloud()


def add_people():
    with driver.session() as session:

        log.info('Adding 3 more Person nodes')
        for first, last in [('Adam', 'Smith'),
                            ('Jonas', 'Salk'),
                            ('Rosalind', 'Franklin')
                            ]:
            cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'})" % (
                first, last)
            session.run(cyph)

        log.info("Now get these people in the DB:")
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for record in result:
            print(record['first_name'], record['last_name'])


def add_colors():
    with driver.session() as session:

        log.info('Adding 3 colors')
        for color in ['blue', 'red', 'green']:
            cyph = "CREATE (n:Color {name:'%s'})" % (color)
            session.run(cyph)

        log.info('Putting the colors into the db')
        cyph = """MATCH (c:Color)
                  RETURN c.name as name
               """
        result = session.run(cyph)
        print('Colors in database:')
        for record in result:
            print(record['name'])


def run_db():
    add_people()
    add_colors()


if __name__ == '__main__':
    run_db()
