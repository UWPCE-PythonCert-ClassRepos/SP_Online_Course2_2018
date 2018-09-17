#!/usr/bin/env python3

import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth
import utilities
import login_database

log = utilities.configure_logger('default', 'logs/neo4j_script.log')

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

prompt = ("\nWhat would you like to do?\n"
          "Choose an action from this list:\n"
          "1 - Add a New Donation\n"
          "2 - Send a Thank You\n"
          "3 - Thank Everyone\n"
          "4 - Create a Report\n"
          "5 - Update an Entry\n"
          "6 - Delete an Entry\n"
          "7 - Quit\n")

donation_dictionary = {'Ted Laws': [100],
                       'Kristin Laws': [150],
                       'Ryan Moore': [600],
                       'Beth Ross': [1000],
                       'Andrew Crawford': [2000, 4000]}


def menu_selection(prompt, dispatch_dict):
    while True:
        response = input(prompt)
        try:
            if dispatch_dict[response]() == "Exit Menu":
                break
        except KeyError:
            print("\nThat was not one of the options.")


def exit():
    return "Exit Menu"


def number_collector(prompt):
    while True:
        try:
            output = int(input(prompt))
            break
        except ValueError:
            print("\nThat wasn't a number value.")
    return output


def populate_db():
    """
        add job data to database
    """
    for donation in [100, 150, 600, 1000, 2000, 4000]:
        add_gift_cyph = "CREATE (d:Donation {Donation_amt: %s})" % (donation)
        session.run(add_gift_cyph)
    for donor in ['Ted Laws',
                  'Kristin Laws',
                  'Ryan Moore',
                  'Beth Ross',
                  'Andrew Crawford']:
        add_donor_cyph = "CREATE (n:Donor {Name:'%s'})" % (donor)
        session.run(add_donor_cyph)
        donations = donation_dictionary[donor]
        for donation in donations:
            relationship_cyph = """MATCH (d1:Donor), (n1:Donation)
                                       WHERE d1.Name='%s'
                                       AND n1.Donation_amt = %s
                                       CREATE (d1)-[d:DONATED]->(n1)
                                       return d1, d, n1
                                """ % (donor, donation)
            session.run(relationship_cyph)


def add_new_donation():

    name = input("\nA new donation! Who donated? (First and Last Name): ")

    cyph = "MERGE (n: Donor {Name:'%s'})" % (name)
    session.run(cyph)

    amount = number_collector("\nHow much did {} donate: ".format(name))

    donation_cyph = """MATCH (d1:Donor)
                       WHERE d1.Name='%s'
                       create (d1)-[d:DONATED]->(g1:Donation {Donation_amt: %s})
                       return d1, d, g1
                    """ % (name, amount)
    session.run(donation_cyph)


def donor_totals(name):
    total_donated = 0
    total_donations = 0
    donations_cyph = """MATCH (d1:Donor)-[d:DONATED]->(donations)
                        WHERE d1.Name = '%s'
                        RETURN donations
                     """ % (name)
    donations_to_sum = session.run(donations_cyph)
    for row in donations_to_sum:
        total_donations += 1
        total_donated += row.values()[0]['Donation_amt']
    return total_donations, total_donated


def write_thank_you(name=""):

    if name == "":
        name = input("\nWho would you like a thank you note for? "
                     "(First and Last Name): ")

    total_donations, total_donated = donor_totals(name)

    if total_donations > 0:
        note = ("Dear {},\n"
                "\nThank you for your generosity to our cause.\n"
                "You have now given {} time(s) for a total of ${:,}."
                "\nWe greatly appreciate your contributions!"
                "\n\nThank you!\nAlex Laws".format(name,
                                                   total_donations,
                                                   total_donated))
        with open("{}.txt".format(name), 'w') as f:
            f.write(note)
    else:
        print("That person has not made any donations.")


def thank_everyone():

    all_cyph = """MATCH (d:Donor)
                  RETURN d.Name as name
               """
    full_result = session.run(all_cyph)

    for donor in full_result:
        write_thank_you(donor['name'])


def build_report():

    print("Donor Name       |  Total Given  |  Num Gifts  |  Average Gift")

    all_cyph = """MATCH (d:Donor)
                  RETURN d.Name as name
               """
    full_result = session.run(all_cyph)
    for donor in full_result:
        total_donations, total_donated = donor_totals(donor['name'])
        avg = total_donated / total_donations
        print("{:17} ${:14,.2f} {:13} ${:13,.2f}".format(donor['name'],
                                                         total_donated,
                                                         total_donations,
                                                         avg))


def update_donor(name):
    full_name = input("What is the correct name: ")
    cyph = """MATCH (d1:Donor)
              WHERE d1.Name='%s'
              set d1.Name='%s'
              return d1:Donor
           """ % (name, full_name)
    session.run(cyph)
    return full_name


def print_donations(name):
    donations_cyph = """MATCH (d1:Donor)-[d:DONATED]->(donations)
                        WHERE d1.Name = '%s'
                        RETURN donations
                     """ % (name)
    donations_to_review = session.run(donations_cyph)
    print("Here are the donations for {}:".format(name))
    for row in donations_to_review:
        print('${:.2f}'.format(row.values()[0]['Donation_amt']))


def update_donation(name):
    print_donations(name)
    gift_to_update = number_collector("Which donation amount would you like to update: ")
    correct_amt = number_collector("How much is the actual donation: ")
    cyph = """MATCH (d1:Donor)-[d:DONATED]->(g1:Donation)
              WHERE d1.Name='%s' and g1.Donation_amt = %s
              set g1.Donation_amt = %s
              return d1:Donor, g1:Donation_amt
           """ % (name, gift_to_update, correct_amt)
    session.run(cyph)


def delete_donation(name):
    print_donations(name)
    gift_to_delete = number_collector("Which donation amount do you need to delete: ")
    cyph = """MATCH (d1:Donor)-[d:DONATED]->(g1:Donation)
              WHERE d1.Name='%s' and g1.Donation_amt = %s
              DELETE d, g1
           """ % (name, gift_to_delete)
    session.run(cyph)


def update_entry():

    which_donor = input("Which Donor account do you want to update: ")

    cyph = """MATCH (d1:Donor)
              WHERE d1.Name='%s'
              return d1.Name
           """ % (which_donor)
    donor_to_update = session.run(cyph)

    if donor_to_update:
        what_update = input("Do you want to update a donation or the donor "
                            "record (enter Donor, Donation, or both): ")
        if what_update == "Donor":
            update_donor(donor_to_update.values()[0][0])
        elif what_update == "Donation":
            update_donation(donor_to_update.values()[0][0])
        elif what_update == "Both":
            new_name = update_donor(donor_to_update.values()[0][0])
            update_donation(new_name)
        else:
            print("Please select an option. Try again.")
    else:
        print('That person is not in our records. Please add a new entry.')


def delete_entry():

    which_donor = input("Which Donor account contains the entry "
                        "you need to delete: ")

    cyph = """MATCH (d1:Donor)
              WHERE d1.name='%s'
              return d1:Donor
           """ % (which_donor)
    donor_to_review = session.run(cyph)

    if donor_to_review:
        what_delete = input("Do you want to delete a donation or the entire "
                            "donor record (enter Donor or Donation): ")
        if what_delete == "Donor":
            session.run("""MATCH (n {Name: '%s'})
                           DETACH DELETE n
                        """ % (which_donor))
        elif what_delete == "Donation":
            delete_donation(which_donor)
        else:
            print("Please select an option. Try again.")
    else:
        print('That person is not in our records. No need to delete.')


menu_dict = {"1": add_new_donation, "2": write_thank_you,
             "3": thank_everyone, "4": build_report,
             "5": update_entry, "6": delete_entry, "7": exit}

if __name__ == '__main__':
    driver = login_database.login_neo4j_cloud()
    with driver.session() as session:
        log.info('Step 1: First, clear the entire database, so we can start over')
        log.info("Running clear_all")
        session.run("MATCH (n) DETACH DELETE n")
        populate_db()
        menu_selection(prompt, menu_dict)
