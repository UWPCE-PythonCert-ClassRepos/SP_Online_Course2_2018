from pprint import pprint as pp
import mr_login_database
import mr_utilities
import logging
import sys
import json
from neo4j.v1 import GraphDatabase
import random


log = logging.getLogger("neo4j.bolt")
log.setLevel(logging.INFO)

driver = mr_login_database.login_neo4j_cloud()
with driver.session() as session:
    session.run("MATCH (n) DETACH DELETE n")


with driver.session() as session:
    donors = (
        "Bob Dylan",
        "Tom Petty",
        "Bruce Springsteen",
        "Haley Coment",
        "Moonbeam Moon"
    )
    for donor in donors:
        cyph = """CREATE (:Person {{Name: '{}'}})
        """.format(donor)
        session.run(cyph)
    print('Check if donors were added to db')
    cyph = """MATCH (person:Person)
                RETURN person.Name as Name
    """
    results = session.run(cyph)


    for record in results:
        print(record['Name'])
    for donor in donors:
        # Every person made 3 donations
        for x in range(0,3):
            cyph = """
                MATCH (person:Person {{Name: '{}'}})
                CREATE (person)-[donated:DONATED]->(d:Donations {{Amount: {}}})
                RETURN person
            """.format(donor, random.randint(5, 99999))
            
            session.run(cyph)

    print('Check if donations were added')

    cyph = """
    MATCH (person:Person)
    return person
    """
    results = session.run(cyph)
    all_donors = []
    for record in results:
        all_donors.append(record['person']['Name'])
    print('All Donors: {}'.format(all_donors))
    for donor in all_donors:
        cyph = """
        MATCH (person:Person {{Name: '{}'}})
        -[:DONATED]-> (donation_amount)
        RETURN donation_amount
        """.format(donor)
        results = session.run(cyph)
        for record in results:
            print('{} has donated: ${}'.format(
                donor,
                record['donation_amount']['Amount']
            ))
    
def main_menu():
    
    main_menu_dict = {'1': thank_you, 
                      '2': print_list_donors,
                      '3': create_report, 
                      '4': delete_donor,
                      '5': quit
                      }
    
    main_prompt = 'Enter 1-5 from the following options:\n\
                   (1) Add A Donation from a New or Existing Donor\n\
                   (2) List All Donors\n\
                   (3) Create Report\n\
                   (4) Delete Donor\n\
                   (5) Exit\n\
                   >> ' 
    main_menu_response(main_prompt, main_menu_dict)


def main_menu_response(prompt, main_menu_dict):
    while True:
        response = input(prompt)
        try:
            if main_menu_dict[response]() == "exit menu":
                print("Have a nice day...")
                sys.exit(0)
        except KeyError:
            print("Enter a number between 1-5.")    

def quit():
    return 'exit menu'


def list_donors():

    driver = mr_login_database.login_neo4j_cloud()
    with driver.session() as session:
        cyph = """
                MATCH (person:Person)
                return person
                """
        results = session.run(cyph)
        all_donors = []
        for donor in results:
            all_donors.append(donor['Person']['Name'])
    return all_donors

def print_list_donors():

    donors = list_donors()
    for donor in donors:
        print(donor)

def thank_you():

    driver = mr_login_database.login_neo4j_cloud()
    donor_lis = list_donors()
    with driver.session() as session:
        name = donor_name_prompt()
        if name in donor_lis:
            print(f'{name} is a previous donor.')
            donation = donation_prompt()
            cyph = update_donations(name, donation)
            session.run(cyph)
            print(f'Donation from {name} added successfuly.')
            print(thank_you_message(name, donation))
            return

        else:
            print(f'{name} is a new donor!')
            donation = donation_prompt()
            cyph = update_donations(name, donation)
            session.run(cyph)
            print(thank_you_message(name, donation))
            return            
    
        
def donor_name_prompt():
    reply = input('Enter the first and last name of the donor or enter ''list'' to see a list of previous donor names or enter Q to exit to main menu\n> ')          
    if reply.lower() == 'list':
        print_list_donors()
        main_menu()
    elif reply.upper() == 'Q':
        main_menu()
    else:
        first, last = reply.split(' ')
        full_name = first.title() + ' ' + last.title()
        return full_name

def update_donations(name, donation):
    cyph = """
    MATCH (person: Person {{Name: '{}'}})
    CREATE (person) -[:DONATED]-> (d:Donations {{Amount: {}}})
    RETURN person
    """.format(name, donation)
    return cyph

def donor_nickname_prompt():
    return input('Enter the nickname of the donor\n>> ')

def donation_prompt():
    donation = float(input('Enter the donation amount: '))
    return donation


def thank_you_message(name, donation):
        return f"Thank you {name} for your generous support for our charity! Your genereous donation of ${float(donation):.2f} is much appreciated."

def delete_donor():

    driver = mr_login_database.login_neo4j_cloud()
    list_d = list_donors()
    while True:
        with driver.session() as session:
            name = donor_name_prompt()
            if name in list_d:
                del_donor = "match(person:Person {Name: '%s'}) delete person" % (name)
                session.run(del_donor)
                print(f'{name} successfuly deleted from database.')
                return
            else:
                print(f'{name} is not in the database! Please try again.')


def total_donations(donor):
    driver = mr_login_database.login_neo4j_cloud()
    with driver.session() as session:
        cyph = """
                MATCH (person:Person {{donor_name: '{}'}})
                -[:DONATED]-> (donation_amount)
                RETURN donation_amount
                """.format(donor)
        results = session.run(cyph)
        all_donations = []
        for donor in results:
            all_donations.append(donor['donation_amount']['Amount'])
            print(f'{donor} and {all_donations}')
            
    return sum(all_donations)


def create_report():
    
    driver = mr_login_database.login_neo4j_cloud()
    list_d = list_donors()
    with driver.session() as session:
        for donor in list_d:
            try:
                print('{:20} | {:15}'.format(
                donor, get_total_for_donor(donor)))
                return
            except TypeError:
                pass
        
if __name__ == '__main__':

    main_menu()

