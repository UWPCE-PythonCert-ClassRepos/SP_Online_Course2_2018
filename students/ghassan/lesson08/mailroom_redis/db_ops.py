import login_database
import utilities
import json


log = utilities.configure_logger('default', '../db_ops.log')


def update_donations(donor, donation):
    log.info('Updating donations')
    r = login_database.login_redis_cloud()
    rcrds = json.loads(r.get('donors'))
    for record in rcrds:
        if record['donor_name'] == donor:
            record['donations'].append(donation)
            log.info('{} has donated: {}'.format(donor, record))
    log.info('Records to be added: {}'.format(rcrds))
    log.info('Updating records')
    r.set('donors', json.dumps(rcrds))
    log.info('Check if the db was updated')
    log.info(json.loads(r.get('donors')))


def list_donors():
    log.info('Listing all donors')
    r = login_database.login_redis_cloud()
    all_donors = []
    rcrds = json.loads(r.get('donors'))
    for record in rcrds:
        all_donors.append(record['donor_name'])
    log.info(all_donors)
    return all_donors


def get_total_for_donor(donor):
    log.info('Getting total donations for donor: {}'.format(donor))
    r = login_database.login_redis_cloud()
    rcrds = json.loads(r.get('donors'))
    for record in rcrds:
        if record['donor_name'] == donor:
            log.info('{} has donated: {}'.format(donor, sum(record['donations'])))
    return sum(record['donations'])


def send_thankyou(donor):
    print('Thank you {} for your generous donation of {}'.format(
        donor, get_total_for_donor(donor)
    ))


def add_donor(donor):
    log.info('Adding a new donor: {}'.format(donor))
    r = login_database.login_redis_cloud()
    rcrds = json.loads(r.get('donors'))
    rcrds.append({
        'donor_name': donor,
        'donation': []
    })
    r.set('donors', json.dumps(rcrds))


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