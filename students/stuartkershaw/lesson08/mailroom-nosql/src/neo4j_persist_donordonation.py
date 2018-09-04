import pprint

import login_database
import utilities

log = utilities.configure_logger('default', '../logs/neo4j.log')


def create_donor(name):
    """
    Add new donor to database
    """
    log.info('Working with Neo4j create_donor function')

    log.info('Creating Donor record...')

    try:
        driver = login_database.login_neo4j_cloud()

        # with driver.session() as session:
        #   session.run("MATCH (n) DETACH DELETE n")

        with driver.session() as session:
            log.info('Set constraint on donor.id.')

            constraint = "CREATE CONSTRAINT ON (donor:Donor) ASSERT donor.id IS UNIQUE"

            session.run(constraint)

            cyph = "CREATE (p:Donor {donor_name:'%s', id:'%s'})" % (name, name.replace(' ', '_').lower())

            session.run(cyph)

            log.info('Donor created.')

            cyph = """MATCH (p:Donor)
                      RETURN p.donor_name as donor_name, p.id as id
                    """
            result = session.run(cyph)

            print("Donors in database:")

            for record in result:
              print(record)

    except Exception as e:
        log.info(f'Error creating = {name}')
        log.info(e)

    finally:
        log.info('Neo4j create_donor complete')


def update_donor(old_name, new_name):
    """
    Update donor name
    """
    log.info('Working with Neo4j update_donor function')

    log.info('Updating Donor record...')

    try:
        driver = login_database.login_neo4j_cloud()

        with driver.session() as session:
            pass

    except Exception as e:
        log.info(e)

    finally:
        log.info('Neo4j update_donor complete')


def delete_donor(name):
    """
    Delete donor
    """
    log.info('Working with Neo4j delete_donor function')

    log.info('Updating Donor record...')

    try:
        driver = login_database.login_neo4j_cloud()

        with driver.session() as session:
            pass

    except Exception as e:
        log.info(e)

    finally:
        log.info('Neo4j delete_donor complete')


def create_donation(donor, amount):
    """
    Add new donation to database
    """
    log.info('Working with Neo4j create_donation function')

    log.info('Creating Donation record...')

    try:
        driver = login_database.login_neo4j_cloud()

        with driver.session() as session:
            donor_id= donor.replace(' ', '_').lower()

            cyph = "CREATE (d:Donation {donation_amount:'%s', donor_id:'%s'})" % (amount, donor_id)

            session.run(cyph)

            log.info('Donation created.')

            cyph = """MATCH (d:Donation)
                      RETURN d.donation_amount as donation_amount, d.donor_id as donor_id
                    """
            result = session.run(cyph)

            log.info('Donations in database:')

            for record in result:
              print(record)

            log.info('Create Donor relationship')

            cypher = """
                MATCH (p:Donor {id:'%s'})
                CREATE (p)-[gave:GAVE]->(d:Donation {donation_amount:'%s', donor_id:'%s'})
                RETURN p
            """ % (donor_id, amount, donor_id)
            session.run(cypher)

            log.info('Print donation relationships.')

            cyph = """
            MATCH (donor {donor_name:'%s', id:'%s'})
                    -[:GAVE]->(donationsGiven)
            RETURN donationsGiven
            """ % (donor, donor_id)

            result = session.run(cyph)

            print("{} {} has given:".format(donor, donor_id))
            
            for rec in result:
                for gave in rec.values():
                    print(gave)

    except Exception as e:
        log.info(f'Error creating = {donor, amount}')
        log.info(e)

    finally:
        log.info('Neo4j create_donation complete')


def update_donation(donor, old_donation, new_donation):
    """
    Update donation amount
    """
    log.info('Working with Neo4j update_donation function')

    log.info('Updating Donation record...')

    try:
        driver = login_database.login_neo4j_cloud()

        with driver.session() as session:
            pass

    except Exception as e:
        log.info(f'Error updating Donation = {donor, old_donation}')
        log.info(e)

    finally:
        log.info('Neo4j update_donation complete')


def delete_donation(donor, donation):
    """
    Delete donation
    """
    log.info('Working with Neo4j delete_donation function')

    log.info('Deleting Donation record...')

    try:
        driver = login_database.login_neo4j_cloud()

        with driver.session() as session:
            pass

    except Exception as e:
        log.info(f'Error deleting Donation = {donor, donation}')
        log.info(e)

    finally:
        log.info('Neo4j update_donation complete')


def get_donor_names():
    """
    Get donor names from database
    """
    log.info('Working with Neo4j get_donor_names function')

    log.info('Querying Donor records...')

    try:
        driver = login_database.login_neo4j_cloud()

        with driver.session() as session:
            donor_names = []

            cyph = """MATCH (d:Donor)
                      RETURN d.donor_name as donor_name
                    """
            result = session.run(cyph)

            for record in result:
                donor_names.append(record['donor_name'])

    except Exception as e:
        log.info(f'Error retrieving Donors')
        log.info(e)

    finally:
        log.info('Neo4j get_donor_names complete')

        return donor_names


def get_donor_donations():
    """
    Get donor donations from database
    """
    log.info('Working with Neo4j get_donor_donations function')

    log.info('Querying Donation records...')

    try:
        driver = login_database.login_neo4j_cloud()

        with driver.session() as session:
            donor_donations = {}

            cyph = """MATCH (d:Donation)
                      RETURN d.donation_amount as donation_amount, d.donor_id as donor_id
                    """
            result = session.run(cyph)

            for record in result:
                donor_id = record['donor_id']
                donation_amount = record['donation_amount']



    except Exception as e:
        log.info(e)

    finally:
        log.info('Neo4j get_donor_donations complete')

        return donor_donations
