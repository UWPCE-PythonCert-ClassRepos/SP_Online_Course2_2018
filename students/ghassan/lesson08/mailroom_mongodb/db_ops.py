import login_database
import utilities
from pprint import pprint as pp


log = utilities.configure_logger('default', '../db_ops.log')


def update_donations(donor, donation):
    log.info('Updating donations')
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        mailroom = db['mailroom']
        log.info('Getting all donations for donor: {}'.format(donor))
        rcrd = mailroom.find_one(
            {
                'donor_name': donor
            }
        )
        log.info('Record found: {}'.format(rcrd))
        all_donations = rcrd['donations']
        log.info('Donations: {}'.format(all_donations))
        all_donations.append(donation)
        log.info('New Donations: {}'.format(all_donations))
        log.info('New record: {}'.format(rcrd))
        mailroom.find_one_and_update(
            {"_id": rcrd["_id"]},
            {'$set': {"donations": rcrd["donations"]}}
        )
        log.info('Check if the record was updated')
        new_rcrd = mailroom.find_one(
            {
                'donor_name': donor
            }
        )
        log.info('New record from DB: {}'.format(new_rcrd))


def list_donors():
    log.info('Listing all donors')
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        mailroom = db['mailroom']
        rcrd = mailroom.find()
        all_donors = []
        for item in rcrd:
            all_donors.append(item['donor_name'])
        pp(all_donors)
        return all_donors


def get_total_for_donor(donor):
    log.info('Getting total donations for donor: {}'.format(donor))
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        mailroom = db['mailroom']
        log.info('Getting all donations for donor: {}'.format(donor))
        rcrd = mailroom.find_one(
            {
                'donor_name': donor
            }
        )
        log.info('Record found: {}'.format(rcrd))
        all_donations = rcrd['donations']
        log.info('Total is: {}'.format(sum(all_donations)))
        return sum(all_donations)


def send_thankyou(donor):
    print('Thank you {} for your generous donation of {}'.format(
        donor, get_total_for_donor(donor)
    ))


def add_donor(donor):
    log.info('Adding a new donor: {}'.format(donor))
    with login_database.login_mongodb_cloud() as client:
        db = client['dev']
        mailroom = db['mailroom']
        mailroom.insert(
            {
                'donor_name': donor,
                'donations': []
            }
        )
        log.info('Check if {} was added: {}'.format(
            donor,
            mailroom.find_one(
                {
                    'donor_name': donor
                })))


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