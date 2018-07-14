import login_database
import utilities
import json


log = utilities.configure_logger('default', '../db_ops.log')


def update_donations(donor, donation):
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        log.info('Updating donations')
        cyph = """
        MATCH (person: Person {{donor_name: '{}'}})
        CREATE (person) -[:DONATED]-> (d:Donations {{amount: {}}})
        RETURN person
        """.format(donor, donation)
        session.run(cyph)


def list_donors():
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        log.info('List donors')
        cyph = """
                MATCH (person:Person)
                return person
                """
        results = session.run(cyph)
        all_donors = []
        for record in results:
            all_donors.append(record['person']['donor_name'])
        log.info('All Donors: {}'.format(all_donors))
    return all_donors


def get_total_for_donor(donor):
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        log.info('Getting total donations for donor: {}'.format(donor))
        cyph = """
                MATCH (person:Person {{donor_name: '{}'}})
                -[:DONATED]-> (donation_amount)
                RETURN donation_amount
                """.format(donor)
        results = session.run(cyph)
        all_donations = []
        for record in results:
            all_donations.append(
                record['donation_amount']['amount']
            )
        log.info('{} has donated a total of: {}'.format(
            donor,
            sum(all_donations)
        ))
    return sum(all_donations)



def send_thankyou(donor):
    print('Thank you {} for your generous donation of {}'.format(
        donor, get_total_for_donor(donor)
    ))


def add_donor(donor):
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        log.info('Adding a new donor: {}'.format(donor))
        cyph = """CREATE (:Person {{donor_name: '{}'}})
                    """.format(donor)
        session.run(cyph)


def create_report():
    print('{:20} | {:15}'.format(
        'Donor Name', 'Total Given'))
    print('-'*70)
    for donor in list_donors():
        try:
            print('{:20} | {:15}'.format(
                donor,
                get_total_for_donor(donor)))
        except TypeError:
            pass


def save_report():
    for donor in list_donors():
        with open(donor + '.txt', 'w') as donorfh:
            try:
                donorfh.write(send_thankyou(donor))
            # In case a donor has no donations
            except TypeError:
                pass