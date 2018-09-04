import pprint

import login_database
import utilities

log = utilities.configure_logger('default', '../logs/mongodb.log')


def create_donor(name):
    """
    Add new donor to database
    """
    log.info('Working with Mongo create_donor function')

    log.info('Creating Donor record...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            db = client['mailroom']

            donors = db['donors']

            donors.insert_one({
                '_id': name.replace(' ', '_').lower(),
                'donor_name': name
            })

            query = {'donor_name': name}
            results = donors.find(query)

            log.info('Donor created.')

            for r in results:
                pprint.pprint(r)

    except Exception as e:
        log.info(f'Error creating = {name}')
        log.info(e)

    finally:
        log.info('Mongo create_donor complete')


def update_donor(old_name, new_name):
    """
    Update donor name
    """
    log.info('Working with Mongo update_donor function')

    log.info('Updating Donor record...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            db = client['mailroom']

            donors = db['donors']
            donations = db['donations']

            log.info('Add new Donor with updated name...')

            donors.insert_one({
                '_id': new_name.replace(' ', '_').lower(),
                'donor_name': new_name
            })

            log.info('Point old Donor Donations to new Donor document...')

            donations_query = {'donor_id': old_name.replace(' ', '_').lower()}
            donations_update = {'$set': {'donor_id': new_name.replace(' ', '_').lower()}}

            donations.update_many(donations_query, donations_update)

            log.info('Remove old Donor...')

            donor_query = {'_id': old_name.replace(' ', '_').lower()}

            donors.remove(donor_query)

    except Exception as e:
        log.info(e)

    finally:
        log.info('Mongo update_donor complete')


def delete_donor(name):
    """
    Delete donor
    """
    log.info('Working with Mongo delete_donor function')

    log.info('Updating Donor record...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            db = client['mailroom']

            donors = db['donors']
            donations = db['donations']

            log.info('Remove old Donor...')

            donor_query = {'_id': name.replace(' ', '_').lower()}

            donors.remove(donor_query)

            log.info('Remove old Donor Donations...')

            donations_query = {'donor_id': name.replace(' ', '_').lower()}

            donations.remove(donations_query)

    except Exception as e:
        log.info(e)

    finally:
        log.info('Mongo delete_donor complete')


def create_donation(donor, amount):
    """
    Add new donation to database
    """
    log.info('Working with Mongo create_donation function')

    log.info('Creating Donation record...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            db = client['mailroom']

            donations = db['donations']

            donations.insert_one({
                'donation_amount': amount,
                'donor_id': donor.replace(' ', '_').lower()
            })

            query = {'donation_amount': amount}
            results = donations.find(query)

            log.info('Donor created.')

            for r in results:
                pprint.pprint(r)

    except Exception as e:
        log.info(f'Error creating = {donor, amount}')
        log.info(e)

    finally:
        log.info('Mongo create_donation complete')


def update_donation(donor, old_donation, new_donation):
    """
    Update donation amount
    """
    log.info('Working with Mongo update_donation function')

    log.info('Updating Donation record...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            db = client['mailroom']

            donations = db['donations']

            log.info('Find the Donations to update...')

            donation_query = {'donation_amount': old_donation}
            donation_update = {'$set': {'donation_amount': new_donation}}

            donations.update(donation_query, donation_update)

    except Exception as e:
        log.info(f'Error updating Donation = {donor, old_donation}')
        log.info(e)

    finally:
        log.info('Mongo update_donation complete')


def delete_donation(donor, donation):
    """
    Delete donation
    """
    log.info('Working with Mongo delete_donation function')

    log.info('Deleting Donation record...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            db = client['mailroom']

            donors = db['donors']
            donations = db['donations']

            log.info('Find the Donations to update...')

            donation_query = {'donation_amount': donation, 'donor_id': donor.replace(' ', '_').lower()}

            donations.remove(donation_query, multi=False)

            log.info('Check the Donor has Donations, otherwise remove Donor...')

            donations_query = {'donor_id': donor.replace(' ', '_').lower()}

            donations_count = donations.count_documents(donations_query)

            if not donations_count > 0:
                donor_query = {'_id': donor.replace(' ', '_').lower()}
                donors.remove(donor_query)


    except Exception as e:
        log.info(f'Error deleting Donation = {donor, donation}')
        log.info(e)

    finally:
        log.info('Mongo update_donation complete')


def get_donor_names():
    """
    Get donor names from database
    """
    log.info('Working with Mongo get_donor_names function')

    log.info('Querying Donor records...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            donor_names = []
            
            db = client['mailroom']

            donors = db['donors']

            cursor = donors.find()

            for doc in cursor:
                donor_names.append(doc['donor_name'])

    except Exception as e:
        log.info(f'Error retrieving Donors')
        log.info(e)

    finally:
        log.info('Mongo get_donor_names complete')

        return donor_names



def get_donor_donations():
    """
    Get donor donations from database
    """
    log.info('Working with Mongo get_donor_donations function')

    log.info('Querying Donation records...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            donor_donations = {}

            db = client['mailroom']

            donors = db['donors']
            donations = db['donations']

            cursor = donations.find()

            for doc in cursor:
                donor_query = {'_id': doc['donor_id']}

                donor = donors.find_one(donor_query)
                donor_name = donor['donor_name']

                try:
                    donor_donations\
                        .setdefault(donor_name,
                                    []).append(float(doc['donation_amount']))

                except Exception as e:
                    log.info(e)

    except Exception as e:
        log.info(e)

    finally:
        log.info('Mongo get_donor_donations complete')

        return donor_donations
