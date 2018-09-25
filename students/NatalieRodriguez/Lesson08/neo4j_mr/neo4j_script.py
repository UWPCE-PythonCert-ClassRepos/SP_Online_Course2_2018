"""
    neo4j script
"""

import login_db
import utilities
import random

log = utilities.configure_logger('default', '../logs/neo4j_script.log')


def run_example():
    driver = login_db.login_neo4j_cloud()
    session = driver.session()

    donor1 = session.run("create (n:Person {first_name: 'Luke', last_name: 'Rodriguez', donation: 500})")
    donor2 = session.run("create (n:Person {first_name: 'Virgil', last_name: 'Ferdinand', donation: 2500})")
    donor3 = session.run("create (n:Person {first_name: 'River', last_name: 'Tails', donation: 3000})")
    donor4 = session.run("create (n:Person {first_name: 'Joseph', last_name: 'Kibson', donation: 4650})")
    donor5 = session.run("create (n:Person {first_name: 'Emily', last_name: 'Connor', donation: 225})")


def donor_input():
    return input("Enter a donor name or enter 'List'" +
                 " for a list of donors.\n>")


def donation_prompt():
    return input("Enter a donation amount:\n>")


def list_donors():
    driver = login_db.login_neo4j_cloud()
    with driver.session() as session:
        donor_names = session.run(
            "match (n:Person)  return n.first_name as first, n.last_name as last, count(*) order by last, first")
        for i in donor_names:
            print(i[0], i[1])


def send_thankyou():
    don_input = None
    while not don_input:
        don_input = donor_input()
        if don_input.lower() == "list":
            list_donors()
            don_input = None

    donation = None
    while not donation:
        try:
            donation = int(donation_prompt())
        except ValueError:
            print("Enter a valid monetary donation.")
    driver = login_db.login_neo4j_cloud()
    with driver.session() as session:
        first = get_first_name(don_input)
        last = get_last_name(don_input)
        session.run(
            "create (n:Person {first_name: '%s', last_name: '%s', donation: %f})" % (first, last, float(donation)))
    print("Thank you {} for your donation of ${}"
          .format(don_input, donation))


def send_thankyou_total(donor, donation):
    return ("Dear {}, \n We are thankful for your donation of ${}. ".format(donor, donation) +
            "We are extremely grateful for your dedication to the protection and " +
            "preservation of the environment. " +
            "Sincerely, " +
            "The Nature Conservancy")


def create_report():
    print('{:20} | {:15} | {:10} | {:15}'.format(
        'Donor Name', 'Total Donations', 'Number of Gifts', 'Average Gift'))
    print('-' * 78)
    driver = login_db.login_neo4j_cloud()
    with driver.session() as session:
        cyph = session.run(
            "match (n:Person) return n.first_name, n.last_name, count(*), sum(n.donation) as sum, avg(n.donation) order by sum desc")
        for i in cyph:
            print('{:20} | {:15} | {:10} | {:15}'.format(
                ' '.join([i[0], i[1]]), i[2],
                i[3],
                i[4]))


def send_letters():
    driver = login_db.login_neo4j_cloud()
    with driver.session() as session:
        cyph = session.run(
            "match (n:Person) return n.first_name, n.last_name, count(*), sum(n.donation) as sum, avg(n.donation)")
        for i in cyph:
            with open('{}.txt'.format(' '.join([i[0], i[1]])), 'w') as donorfh:
                donorfh.write(send_thankyou_total(' '.join([i[0], i[1]]), i[3]))


def close_program():
    print('\nClosing Program.\n')


def delete_donor():
    print('Enter a donor name to delete.\n')
    driver = login_db.login_neo4j_cloud()
    with driver.session() as session:
        try:
            donor_names = session.run(
                "match (n:Person)  return n.first_name as first, n.last_name as last, count(*) order by last, first")
            first_name = input('First Name: ')
            last_name = input('Last Name: ')
            deletion = "match (n:Person {first_name: '%s', last_name: '%s'}) delete n" % (first_name, last_name)
            session.run(deletion)
            print('{} {} has been removed from the database.'.format(first_name, last_name))
        except:
            pass


def get_first_name(fullname):
    firstname = ''
    try:
        firstname = fullname.split()[0]
    except Exception as e:
        print(str(e))
    return firstname


def get_last_name(fullname):
    lastname = ''
    try:
        index = 0
        for part in fullname.split():
            if index > 0:
                if index > 1:
                    lastname += ' '
                lastname += part
            index += 1
    except Exception as e:
        print(str(e))
    return lastname