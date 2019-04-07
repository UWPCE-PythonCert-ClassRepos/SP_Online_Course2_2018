"""
Populate mailroom.db with existing donor data.
"""

import pprint
import login_database


def populate_db(donor_list):

    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        for donor, date_added, donation_list in donor_list:
            cyph = "CREATE (n:Donor {name:'%s', date_added:'%s'})" % (
                donor, date_added)
            session.run(cyph)
            for amount, date_donated in donation_list:
                cyph = "CREATE (n:Donation {amount:%.2f, date:'%s'})" % (
                    amount, date_donated)
                session.run(cyph)
                cyph = """
                    MATCH (d1:Donor {name:'%s'})
                    CREATE (d1)-[donated:DONATED]->(a1:Donation {amount: %.2f, date: '%s'})
                    RETURN d1
                    """ % (donor, amount, date_donated)
                session.run(cyph)


if __name__ == '__main__':

    donors = [
        ('han solo', '2013-11-11', [(3468.34, '2013-11-14'), (457, '2014-11-05'), (34.2, '2018-01-02')]),
        ('luke skywalker', '2017-06-01', [(5286286.3, '2019-03-21'), (567, '2019-03-24'), (23.5678, '2017-07-06')]),
        ('chewbacca', '2011-01-01', [(432, '2011-09-06'), (679.4553, '2013-05-24')]),
        ('princess leia', '2008-12-29', [(5.3434, '2009-08-09')]),
        ('bobba fett, bounty hunter', '1954-07-05', [(67, '1954-07-05')])
    ]

    populate_db(donors)
