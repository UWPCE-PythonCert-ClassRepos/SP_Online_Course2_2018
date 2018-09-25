"""
    creates mailroom db in neo4j
"""

from login_database import login_neo4j_cloud


def run_db():
    driver = login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    with driver.session() as session:
        for (first, last, title, donations,
             num_donations) in [('William', 'Gates III', 'Mr.', 150000, 3),
                                ('Sergey', 'Brin', 'Mr.', 150000, 3),
                                ('Vinton', 'Cerf', 'Mr.', 50000, 2),
                                ('Elon', 'Musk', 'Mr.', 100000, 1),
                                ('Timothy', 'Berners-Lee', 'Sir', 50000, 2),
                                ('Anne', 'Wojcicki', 'Ms.', 125000, 1),
                                ('Linda', 'Avey', 'Ms.', 200000, 2)]:
            # cyph = "CREATE (n:Person {first_name:'%s', last_name: '%s'}" +
            # "{title: '%s', donations: '%s', num_donations: '%s'})" % (
            #  first, last, title, donations, num_donations)
            cyph = """
        CREATE (n:Person {first_name: '%s', last_name: '%s', title: '%s', donations: '%s', num_donations: '%s'})""" % (
                first, last, title, donations, num_donations)
            session.run(cyph)

    with driver.session() as session:
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name,
                  p.title as title, p.donations as donations, p.num_donations
                  as num_donations
                """
        result = session.run(cyph)
        print("People in database:")
        for rec in result:
            print(rec['first_name'], rec['last_name'], rec['donations'])


if __name__ == '__main__':
    run_db()
