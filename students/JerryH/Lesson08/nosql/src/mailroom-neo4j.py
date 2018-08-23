#!/usr/bin/env python3
import configparser
from pathlib import Path
import pymongo
import redis
from neo4j.v1 import GraphDatabase, basic_auth
import login_database

import utilities

log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = Path(__file__).parent.parent / '.config/config'
config = configparser.ConfigParser()


def add_donor(name, amount):
    with driver.session() as session:
        
        if name not in get_all_donor_names():
            # session.run("create (n:Person) {full_name: name, donation: amount}")
            # session.run("create (n:Person {full_name: name, donation: [amount]})")
            session.run("create (n:Person {full_name: '%s', donation: [%02.2f]})" % (name, amount))            
            print("{} hasn't donated any before. Adding into Donor table.".format(name))
        else:
            donor_names = session.run("MATCH (n:Person) return n.full_name, n.donation")
            # donor_names = session.run("MATCH (n:Person { full_name: '%s' }) RETURN donation.append(%02.2f)" % (name, amount))
            for d in donor_names:
                # print(d[0], d[1])
                if name == d[0]:
                    d[1].append(amount)
                    session.run("MATCH (n:Person { full_name: '%s' }) SET n.donation = %a" % (name, d[1]))

            print("Found a donor from the database, appending his/her gift amount to the table.")


def get_all_donor_names():
    with driver.session() as session:
        donor_names = session.run("match (n:Person) return n.full_name")
        # for d in donor_names:
        #     print(d[0])
    return [d[0] for d in donor_names]


def list_all_donor_names_sorted():
    return "\n".join(sorted(get_all_donor_names()))


def send_thank_you():
    donor_name = None
    while not donor_name:
        donor_name = donor_name_prompt()
        if donor_name.lower() == "list":
            print(list_all_donor_names_sorted())
            donor_name = None

    donation = None
    while not donation:
        try:
            donation = donation_prompt()
        except ValueError:
            print("Not a valid number! Please enter a valid number:\n")

    # If the donnor doesn't exist in the donor list - add his info
    # if donor_name not in get_all_donor_names():
    try:
        add_donor(donor_name, donation)
    except ValueError:
        print("Please enter both of your \"First Name\" and \"Last Name\"")
    # else:
    #     for donor in self.donors:
    #         if donor.full_name == donor_name:
    #             donor.add_donation(donation)

    print("Thank You Email:  Thanks for the donation!\n\n")


def group_donations():
    report = []  # initialize report
    with driver.session() as session:
        donor_names = session.run("match (n:Person) return n.full_name, n.donation")
        for d in donor_names:
            report.append([d[0], sum(d[1]), len(d[1])])

    # Sort the report based on donations
    return sorted(report, key=lambda r: r[1], reverse=True)


def create_report():
    print("\nDonor Name           |  Total Given | Num Gifts | Average Gift")
    print("---------------------------------------------------------------\n")

    # Create the report
    for donor_report in group_donations():
        print("{:23}${:12.2f}{:10}   ${:12.2f}".format(donor_report[0],
            donor_report[1],
            donor_report[2],
            donor_report[1] / donor_report[2]))
    print("\n")


def delete_donation():
    delete_name = input("Whose first name do you want to delete from the donation database? \n")

    if delete_name in get_all_donor_names():
        with driver.session() as session:
            _del = "match (n:Person {full_name: '%s'}) delete n" % (delete_name)
            session.run(_del)
            print('{} has been removed from the database.'.format(delete_name))
    else:
        print("Can't find the name you want to delete.")


def quit_program():
	print("Thanks for using my script! Bye!")


driver = login_database.login_neo4j_cloud()
with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")

with driver.session() as session:
    # for name, donation in [
    #     # ('Bill Gates', [234.22, 45.24, 453.09, 923.01]),
    #     # ('Jeff Bezo', [435.34]),
    #     # ('Mike Dell', [299.89, 98.01]),
    #     # ('Harry Potter', [999.34, 100]) 
    #     # ]:
    #     ('Bill Gates', 100),
    #     ('Mike Dell', 200),
    #     ('Jason Williams', 598.09),
    #     ('Mike Dell', 345.33)
    #     ]:

    #     cyph = "CREATE (n:Person {full_name:'%s', gift_values: '%s'})" % (
    #             name, donation)
    #     session.run(cyph)

    # cyph = """MATCH (p:Donor)
    #               RETURN p.full_name as full_name, p.gift_values as gift_values
    #         """
    # result = session.run(cyph)
    # print('Donor in database....')
    # for record in result:
    #     print(record['full_name'], record['gift_values'])
    p1 = session.run("create (n:Person {full_name: 'Bill Gates', donation: [100, 2034.90]})")
    p2 = session.run("create (n:Person {full_name: 'Mike Dell', donation: [200]})")
    p3 = session.run("create (n:Person {full_name: 'Jeff Bezo', donation: [678.99, 873274.22]})")
    p4 = session.run("create (n:Person {full_name: 'Harry Potter', donation: [900.87]})")

    # donor_names = session.run("match (n:Person) return n.full_name, n.donation")

    # for d in donor_names:
    #     print(d[0], d[1])



QUIT_OPT = '4'

selection_map = {
    "1": send_thank_you,
    "2": create_report,
    # "3": db.send_letters,
    "3": delete_donation,
    "4": quit_program
    # "5": db.challenge_report,
    # "6": db.projections
}

menu = {
    'op1': "Send a Thank You",
    'op2': "Create a Report",
    # 'op3': "Send Letters To Everyone",
    'op3': "Delete a donation",
    'op4': "Quit"
    # 'op5': "Challenge",
    # 'op6': "Run Projections"
}

def prompt():
    return input("\nPlease choose the following options:\n1) {op1}.\n2) {op2}.\n3)"
        " {op3}.\n4) {op4}.\n".format(**menu))
        # " {op3}.\n4) {op4}.\n5) {op5}.\n6) {op6}.\n".format(**menu))


def donation_prompt():
    return float(input("Please enter the donation amount:\n"))


def donor_name_prompt():
    return input("Send a Thank You - Please enter a full name or type \"list\""
        "to list the current donors:\n")

def challenge_prompt():
    return int(input("What's your challenge factor?\n"))

def min_donation_prompt():
    return int(input("What's minimum donation you want to set? (Default is $1000)\n"))

def main():
    option_value = 0
    while option_value != QUIT_OPT:
        try:
            option_value = prompt()
            selection_map[option_value]()
        except KeyError:
            print("%s is not a valid option! Please try again.\n" % option_value)


# start the script
if __name__ == "__main__":
    main()

