import logging
import login_db
import utilities

log = utilities.configure_logger('default', '../logs/mongodb_script.log')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_example(donor_items):
    """
    mongodb data manipulation
    """

    with login_db.login_mongodb_cloud() as client:
        log.info('Calling donor database.')
        log.info('If it does not exist, mongodb shall create it.')
        db = client['donors']

        log.info('Inside database, there is a module called Donor')
        log.info('If it does not exist, mongodb shall create it.')

        donor = db['donor']

        log.info('Adding data from the dict.')
        donor.insert_many(donor_items)

    return donor


def donor_input():
    return input("Enter a donor name or enter 'List'" +
                 " for a list of donors.\n>")


def donation_prompt():
    return input("Please enter a donation amount. \n>")


def list_donors(donor):
    log.info('Retrieving all donors.')
    for i in donor.find():
        print(i['name'])


def send_thankyou(donor):
    don_input = None
    while not don_input:
        don_input = donor_input()
        if don_input.lower() == "list":
            list_donors(donor)
            don_input = None

    donation = None
    while not donation:
        try:
            donation = int(donation_prompt())
        except ValueError:
            print("Enter a valid monetary donation.")
    found = False
    for i in donor.find():
        if don_input == str(i['name']):
            donation_old = int(i['donation'])
            donation_new = donation_old + donation
            count_old = i['count']
            count_new = count_old + 1
            average_old = int(i['average'])
            donor.update_one({'name': don_input,
                              'donation': donation_old,
                              'average': donation_old / count_old,
                              'count': count_old
                              }, {'$set':
                                      {'name': don_input,
                                       'donation': donation_new,
                                       'average': donation_new / count_new,
                                       'count': count_new
                                       }})
            found = True
    if found == False:
        new_donor = {'name': don_input,
                     'donation': donation,
                     'average': donation,
                     'count': 1}
        donor.insert_one(new_donor)
    print("Thank you, {} for your donation of ${}."
          .format(don_input, donation))


def send_thankyou_total(donor, donation):
    return ("Dear {}, \n We are thankful for your donation of ${}. ".format(donor, donation) +
            "We are extremely grateful for your dedication to the protection and " +
            "preservation of the environment. " +
            "Sincerely, " +
            "The Nature Conservancy")


def create_report(donor):
    print('{:20} | {:15} | {:10} | {:15}'.format(
        'Donor Name', 'Total Donations', 'Number of Gifts', 'Average Gift'))
    print('-' * 78)
    for i in donor.find():
        try:
            print('{:20} | {:15} | {:10} | {:15}'.format(
                i['name'], i['donation'],
                i['average'],
                i['count']))
        except TypeError:
            pass


def send_letters(donor):
    for i in donor.find():
        with open('{}.txt'.format(i['name']), 'w') as donorfh:
            donorfh.write(send_thankyou_total(str(i['name']), str(i['donation'])))


def close_program(donor):
    print('\nClosing Program\n')


def delete_donor(donor):
    """
    mongodb data
    """
    don_input = None
    while not don_input:
        don_input = donor_input()
        if don_input.lower() == "list":
            list_donors(donor)
            don_input = None
        else:
            check = donor.count_documents({'name': don_input}) > 0
            if check:
                donor.delete_many({'name': don_input})
            else:
                print("{} is not in the donor database.".format(don_input))