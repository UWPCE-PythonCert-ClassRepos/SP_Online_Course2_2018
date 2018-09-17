"""
    people and colors assignment using neo4j
"""

import utilities
import login_database
import neo4j_script


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

        color_list = ['blue', 'red', 'green']
        log.info('Adding 3 colors')
        for color in color_list:
            cyph = "CREATE (c:Color {name:'%s'})" % (color)
            session.run(cyph)

        log.info('Putting the colors into the db')
        cyph = """MATCH (c:Color)
                  RETURN c.name as name
               """
        result = session.run(cyph)
        print('Colors in database:')
        for record in result:
            print(record['name'])


def match_people_colors():
    blue_list = [('Fred', 'Barnes'), ('Jonas', 'Salk'),
                 ('Rosalind', 'Franklin')]
    red_list = [('Marie', 'Curie'), ('Nancy', 'Cooper'), ('Mary', 'Evans'),
                ('Adam', 'Smith')]
    green_list = [('Alice', 'Cooper'), ('Bob', 'Jones')]
    # color_list = [blue_list, red_list, green_list]

    with driver.session() as session:

        log.info('Associating people with their respective favorite color')
        # for lst in color_list:
        #     color = str(lst).strip('_list')
        for first, last in blue_list:
            cypher = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[favorite_color:COLOR]->(c:Color {name:'blue'})
              RETURN p
            """ % (first, last)
            session.run(cypher)
        for first, last in red_list:
            cyph = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[favorite_color:COLOR]->(c:Color {name:'red'})
              RETURN p
            """ % (first, last)
            session.run(cyph)
        for first, last in green_list:
            cypher = """
              MATCH (p:Person {first_name:'%s', last_name:'%s'})
              CREATE (p)-[favorite_color:COLOR]->(c:Color {name:'green'})
              RETURN p
            """ % (first, last)
            session.run(cypher)

        try:
            cyph = """
              MATCH (blue:Color {name:'blue'})<-[:COLOR]-(p)
              RETURN p.first_name as first_name, p.last_name as last_name
            """
            result = session.run(cyph)
            print("\nBlue is the favorite color of these people:")
            for record in result:
                print(record['first_name'], record['last_name'])

            cypher = """
              MATCH (red:Color {name:'red'})<-[:COLOR]-(p)
              RETURN p.first_name as first_name, p.last_name as last_name
            """
            result = session.run(cypher)
            print("\nRed is the favorite color of these people:")
            for record in result:
                print(record['first_name'], record['last_name'])

            cyph = """
              MATCH (green:Color {name:'green'})<-[:COLOR]-(p)
              RETURN p.first_name as first_name, p.last_name as last_name
            """
            result = session.run(cyph)
            print("\nGreen is the favorite color of these people:")
            for record in result:
                print(record['first_name'], record['last_name'])

        except Exception as e:
            print(f'neo4j error: {e}')


def run_db():
    neo4j_script.run_example()
    add_people()
    add_colors()
    match_people_colors()


if __name__ == '__main__':
    run_db()
