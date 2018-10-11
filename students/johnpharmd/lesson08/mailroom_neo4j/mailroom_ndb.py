"""
    creates mailroom db in neo4j
"""

import sys
from login_database import login_neo4j_cloud


driver = login_neo4j_cloud()


def populate_db():
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
            cyph = """
        CREATE (n:Person {first_name: '%s', last_name: '%s', title: '%s', donations: '%s', num_donations: '%s'})""" % (
                first, last, title, donations, num_donations)
            session.run(cyph)


def get_all_donors():
    with driver.session() as session:
        cyph = """MATCH (p:Person)
                  RETURN p.first_name as first_name, p.last_name as last_name
                """
        result = session.run(cyph)
        print("People in database:")
        for rec in result:
            print(rec['first_name'], rec['last_name'])


def get_one_donor_data():
    while True:
        title = input('Enter donor title: ')
        last_name = input('Enter donor last name, or "e" to exit: ')
        if last_name.lower() == 'e':
            break
        else:
            with driver.session() as session:
                cyph = """
                MATCH (p:Person {title:'%s', last_name:'%s'})
                RETURN p.title as title, p.last_name as last_name,
                p.donations as donations, p.num_donations as num_donations
                """ % (title, last_name)
                result = session.run(cyph)
                print()
                for d in result:
                    print(d['title'], d['last_name'], d['donations'],
                          d['num_donations'], '\n')


class UI():
    def __init__(self):
        menu_dct = {
            '1': get_all_donors,
            '2': get_one_donor_data,
            'q': sys.exit
            }
        main_text = '\n'.join((
            'Choose from the following:',
            '"1" - Get a List of Donors,',
            '"2" - Get Data from All Fields for One Donor, or',
            '"q" to Quit: '
            ))
        while True:
            print('\nMain Menu:')
            response = input(main_text)
            print()
            try:
                if response.lower() == 'q':
                    print('Program execution completed.')
                menu_dct[response]()

            except KeyError:
                print('\nThat selection is invalid. Please try again.')


if __name__ == '__main__':
    populate_db()
    interaction_instance = UI()
