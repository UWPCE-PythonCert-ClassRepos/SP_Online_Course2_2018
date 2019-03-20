#!/usr/bin/env python3

import os
from donor_models import Donor_obj
import login_database

MAIN_PROMPT = ("\nWould you like to:\n"
               "1 - Send a Thank You\n"
               "2 - Create a Report\n"
               "3 - Modify or Delete donor information\n"
               "4 - Modify or Delete a donation for a specific donor\n"
               "5 - Quit\n")


def list_donors():
    """
    return list of donor names in database
    """
    cyph = """MATCH (p:Person)
              RETURN p.name as name, p.amount as amount
            """
    result = session.run(cyph)
    donor_list = []
    for record in result:
        if record['name'] not in donor_list:
            donor_list.append(record['name'])

    return donor_list


def add_donation(donation_amount, donor_name):
    """
    add donation data to database
    """
    cyph = "CREATE (n:Person {name:'%s', amount:'%s'})" % (donor_name, donation_amount)
    session.run(cyph)


def select_donor():
    """
    select a donation from database
    """
    while True:
        search_name = input('Please enter the name of a donor to modify: \n'
                            'for a list of donors, type "list": ')
        if search_name == 'list':
            print(list_donors())
            continue
        else:
            break

    cyph = """MATCH (p:Person {name: '%s'})
              RETURN p.name as name, p.amount as amount""" % (search_name)
    result = session.run(cyph)
    donations = []
    for record in result:
        donations.append(float(record['amount']))
    print('Record Selected: \n')
    print('{:^25}|{:^60}'.format('Donor Name', 'Entry Date'))
    print('{:<25}|{:<60}'.format(search_name, str(donations)))
    print('\n')

    return search_name


def modify_donor():
    """
    delete a donation from database
    """

    name = select_donor()

    while True:
        new_value = input('input the new name for the donor \n'
                          'OR enter "delete" to delete the donor record \n'
                          'CAUTION: DELETING THE DONOR WILL ALSO DELETE ALL DONATIONS FOR THIS DONOR:  ')
        if new_value.lower() == 'delete':
            cyph = """MATCH (p:Person {name: '%s'})
                      DELETE p""" % (name)
            session.run(cyph)
            break
        else:
            cyph = """MATCH (p:Person {name: '%s'})
                      SET p.name = '%s'
                      RETURN p.name as name, p.amount as amount""" % (name, new_value)
            result = session.run(cyph)
            for record in result:
                print('{} has donated ${:.2f}'.format(record['name'], float(record['amount'])))
            break


def modify_donation():
    """
    delete a donation from database
    """
    name = select_donor()

    while True:
        new_value = input('input the new comma separated list of donation amounts to replace the list shown above \n'
                          'OR enter "delete" to delete all of the donations on record: ')
        if new_value.lower() == 'delete':
            donors.update_one(
                            {'_id': obj_id},
                            {"$set": {"amount": []}})
            break
        else:
            try:
                new_list  = [x.strip() for x in new_value.split(',')]
                donation_amount = [float(x) for x in new_list]
            except ValueError:
                print('input must be a string of numerical values or "delete"')
            else:
                cyph = """MATCH (p:Person {name: '%s'})
                          DELETE p""" % (name)
                session.run(cyph)
                for amount in donation_amount:
                    cyph = "CREATE (n:Person {name:'%s', amount:'%s'})" % (name, amount)
                    session.run(cyph)
                break


def thanks():
    while True:
        donor_name = input('Please enter the Full Name of the donor: ')
        if donor_name == 'list':
            print(list_donors())
            continue
        else:
            break
    while True:
        try:
            donation_amount = float(input('Please enter the amount of the donation: '))
        except ValueError:
            print('input for the amount must be a numerical value ')
        else:
            break
    add_donation(donation_amount, donor_name)
    print(f'Dear {donor_name}:')
    print(f'Thank you for your donation of ${donation_amount:.2f} to our charity.')
    print(f'Your contribution will do a great deal to help our worthy cause')


def create_donor_obj(donor_name):
#    with login_database.login_mongodb_cloud() as client:
#    donors = client['mailroom']['donors']
    cyph = """MATCH (p:Person {name: '%s'})
              RETURN p.name as name, p.amount as amount""" % (donor_name)
    result = session.run(cyph)
    donations = []
    for record in result:
        donations.append(float(record['amount']))
    return Donor_obj(donor_name, donations)


def create_report():
    title_str = '{:<20s}|{:^13}|{:^11}|{:>13}'
    bar_str = '-'*60
    entry_str = '{:<20s} ${:>10.2f} {:>11d} ${:>10.2f}'
    report = [title_str.format('Donor Name', 'Total Given',
                               'Num Gifts', 'Average Gift'), bar_str]
    for donor_name in list_donors():
        donor = create_donor_obj(donor_name)
        report.append(entry_str.format(*(donor.donor_name,
                                         donor.total,
                                         donor.count, donor.average)))
        del donor
    return report


def report():
    for row in create_report():
        print(row)


def letters():
    for donor_name in list_donors():
        donor = create_donor_obj(donor_name)
        with open(donor.donor_name+'.txt', 'w') as outfile:
            outfile.write("Dear {:}, \n".format(donor.donor_name))
            outfile.write(f"Thank you for your accumulative donation of ${donor.total:.2f}. \n")
            outfile.write('Your contribution will do a great deal to help our worthy cause')
        del donor


def quit():
    print("Quitting program")
    return "exit menu"


def menu_selection(prompt, dispatch_dict):
    while True:
        try:
            response = input(prompt)
            if dispatch_dict[response]() == "exit menu":
                break
        except KeyError:
            print('input must be one of the following: 1, 2, 3, or 4:')


MAIN_DISPATCH = {
    '1': thanks,
    '2': report,
    '3': modify_donor,
    '4': modify_donation,
    '5': quit
}

if __name__ == '__main__':
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        menu_selection(MAIN_PROMPT, MAIN_DISPATCH)