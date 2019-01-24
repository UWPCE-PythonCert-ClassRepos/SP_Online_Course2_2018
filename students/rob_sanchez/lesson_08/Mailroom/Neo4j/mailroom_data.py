"""
    Data for mailroom_mongo
"""

import login_database


driver = login_database.login_neo4j_cloud()


def get_donor_data():
    """
        Initial Donors
    """

    initial_donors = {'Tom Cruise': [100, 200, 300],
                      'Keanu Reeves': [1400, 1500],
                      'Katy Perry': [4500, 1600],
                      'Adam Sandler': [500, 2400],
                      'Natalie Portman': [330]
                      }

    return initial_donors


def populate_DB():
    """
        Calls the necessary methods to clear and populated the login_database
        using the initial list of donors
    """
    clearDB()
    create_tables()
    create_donation_relationships()


def create_tables():
    """
        Creates both Donor and Donations tables
    """

    with driver.session() as session:

        print('\nCreating donor table...\n')
        for name in [('Tom Cruise'),
                     ('Keanu Reeves'),
                     ('Katy Perry'),
                     ('Adam Sandler'),
                     ('Natalie Portman')
                     ]:
            cyph = "CREATE (n:Donor {donor_name:'%s'})" % (
                name)
            session.run(cyph)

        print('\nCreating donations table...\n')
        for donation in [100, 200, 300, 1400, 1500, 4500, 1600,
                         500, 2400, 330]:
            cyph = "CREATE (n:Donations {donation_amount:'%s'})" % (
                donation)
            session.run(cyph)


def create_donation_relationships():
    """
        Creates the relationships between donors and donations
    """

    with driver.session() as session:

        print('\nCreating donor-donation relationships...\n')

        for donor in get_all_donors():
            donation = get_donor_data()

            for don in donation[donor]:
                rel_cyph = """
                  MATCH (p1:Donor), (d1:Donations)
                  WHERE p1.donor_name='%s' AND d1.donation_amount='%s'
                  CREATE (p1)-[r:DONATED]->(d1)
                  RETURN p1, r, d1
                """ % (donor, don)

                session.run(rel_cyph)


def get_all_donors():
    """
        Returns a list of all donors
    """

    donor_list = []

    with driver.session() as session:

        cyph = """MATCH (p:Donor)
                  RETURN p.donor_name as donor
                """
        result = session.run(cyph)

        for record in result:
            donor_list.append(record['donor'])

    return donor_list


def get_all_donations(name):
    """
        Returns a list of all donations from the specified donor
    """

    donations_list = []

    with driver.session() as session:

        cyph = """
          MATCH (donor {donor_name:'%s'})-[r:DONATED]->(donation)
          RETURN donation
          """ % (name)

        result = session.run(cyph)

        for record in result:
            for i in record.values():
                donations_list.append(i['donation_amount'])

    return donations_list


def clearDB():
    """
        Clears the entire database
    """
    print('\nClearing the entire database, so we can start over...\n')

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
