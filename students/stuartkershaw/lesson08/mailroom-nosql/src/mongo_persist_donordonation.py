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
            log.info('Step 1: We are going to use a database called mailroom')
            db = client['mailroom']

            log.info('And in that database use a collection called donors')
            donors = db['donors']

            log.info('And in that collection specify a unique index on donor_name')
            donors.create_index('donor_name', unique=True)

            log.info('Step 2: Now we add a donor with the given name')
            donors.insert_one({
                'donor_name': name
            })

            log.info('Step 3: Query to ensure the donor was created')
            query = {'donor_name': name}
            results = donors.find(query)

            log.info('Step 4: Print the results')
            print('Donor created.')
            for r in results:
                pprint.pprint(r)

            db.drop_collection('donors')

    except Exception as e:
        log.info(f'Error creating = {name}')
        log.info(e)

    finally:
        log.info('Mongo create_donor complete')


def update_donor(old_name, new_name):
    """
    Update donor name
    """
    pass


def delete_donor(name):
    """
    Delete donor
    """
    pass


def create_donation(donor, amount):
    """
    Add new donation to database
    """
    log.info('Working with Mongo create_donation function')

    log.info('Creating Donation record...')

    try:
        database = login_database.login_mongodb_cloud()

        with database as client:
            log.info('Step 1: We are going to use a database called mailroom')
            db = client['mailroom']

            log.info('And in that database use a collection called donations')
            donations = db['donations']

            log.info('Step 2: Now we add a donation with the given donor name and amount')
            donations.insert_one({
                'donation_amount': amount,
                'donor_name': donor
            })

            log.info('Step 3: Query to ensure the donation was created')
            query = {'donation_amount': amount}
            results = donations.find(query)

            log.info('Step 4: Print the results')
            print('Donation created.')
            for r in results:
                pprint.pprint(r)

            db.drop_collection('donations')

    except Exception as e:
        log.info(f'Error creating = {donor, amount}')
        log.info(e)

    finally:
        log.info('Mongo create_donation complete')


def update_donation(donor, old_donation, new_donation):
    """
    Update donation amount
    """
    pass


def delete_donation(donor, donation):
    """
    Delete donation
    """
    pass


def get_donor_names():
    """
    Get donor names from database
    """
    pass


def get_donor_donations():
    """
    Get donor donations from database
    """
    pass
