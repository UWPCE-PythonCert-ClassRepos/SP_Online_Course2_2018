import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth


class Donor:
    """
        Donor class is a convenience class to abstract
        away the details of how the actual saving and
        loading is done. Basically, the rest of the mailroom
        operates on the donor class, but the actual saving
        is not guaranteed have the capabilities of this donor
        class, so this class mediates the 2 methodologies.
    """

    def __init__(self, firstname, lastname, donations=[]):
        self.name = (firstname, lastname)
        self.donations = donations

    def add_donation(self, amount):
        self.donations.append(amount)

    def get_donations(self):
        return self.donations

    def get_key(self):
        return self.name

    def get_name(self):
        return "{0} {1}".format(*self.name)

    def get_name_tuple(self):
        return self.name


def login_neo4j_cloud():
    """
        connect to neo4j and login

    """

    config_file = Path(__file__).parent / '.config/config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-gjhedagffggcgbkeokalabbl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver

class DonorCollection:
    """
        Encapsulates the db. Gets data from it
        and returns the data as a Donor. Inserts data
        when necessary.
    """

    def __init__(self):
        self.driver = login_neo4j_cloud()
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def get_donors(self):
        # Get all the people
        cypher = "MATCH (p:Person) "
        cypher += "RETURN p.first_name as firstname, p.last_name as lastname"
        people = self.driver.session().run(cypher)

        for p in people:
            # Create a donor with this name
            firstname = p['firstname']
            lastname = p['lastname']
            donor = Donor(firstname, lastname, list())
            # Get that person's donations
            cypher = f"MATCH (p:Person {{first_name: '{firstname}', last_name:'{lastname}'}}) "
            cypher += "MATCH (p)-[d:DONATED]->(donation:Donation) "
            cypher += "RETURN donation.amount as amount"
            donations = self.driver.session().run(cypher)

            # Create the donation list for this donor
            for d in donations:
                donor.add_donation(float(d['amount']))
            # Return
            yield donor

    def add_donation(self, firstname, lastname, amount):
        amount_float = float(amount)
        # Create the donation
        cypher = f"CREATE (donation:Donation {{amount:'{amount_float}'}}) "
        # Get the person (or create one if it doesn't exist)
        cypher += f"MERGE (p:Person {{first_name:'{firstname}', last_name:'{lastname}'}}) "
        # Now create the donation relationship
        cypher += "CREATE (p)-[d:DONATED]->(donation) "
        cypher += "RETURN p"
        # Run the cypher
        self.driver.session().run(cypher)

    def delete_donor(self, firstname, lastname):
        # Get the person
        cypher = f"MATCH (p:Person {{first_name:'{firstname}', last_name:'{lastname}'}}) "
        # Get the person's donations
        cypher += "MATCH (p)-[d:DONATED]->(donation:Donation) "
        # Delete the donations
        cypher += "DETACH DELETE donation "
        # Delete that person
        cypher += "DELETE p "
        # Run the cypher
        self.driver.session().run(cypher)

    def get_donations(self, firstname, lastname):
        # Get the person
        cypher = f"MATCH (p:Person {{first_name:'{firstname}', last_name:'{lastname}'}}) "
        # Get the person's donations
        cypher += "MATCH (p)-[d:DONATED]->(donation:Donation) "
        cypher += "RETURN donation.amount as amount"
        # Run the cypher
        records = self.driver.session().run(cypher)

        donations_list = list()
        for r in records:
            donations_list.append(float(r['amount']))
        return donations_list

    def delete_donation(self, firstname, lastname, delete_num):
        donations_list = self.get_donations(firstname, lastname)
        if delete_num < len(donations_list):
            amount = donations_list[delete_num]
            # Get the person
            cypher = f"MATCH (p:Person {{first_name:'{firstname}', last_name:'{lastname}'}}) "
            # Get the donations
            cypher += f"MATCH (p)-[d:DONATED]->(donation:Donation {{amount: '{amount}'}}) "
            # Delete that donation
            cypher += "DETACH DELETE donation "
            # Run the cypher
            self.driver.session().run(cypher)

    def change_donation(self, firstname, lastname, change_num, new_amount):
        donations_list = self.get_donations(firstname, lastname)
        if change_num < len(donations_list):
            amount = donations_list[change_num]
            # Get the person
            cypher = f"MATCH (p:Person {{first_name:'{firstname}', last_name:'{lastname}'}}) "
            # Get the donations
            cypher += f"MATCH (p)-[d:DONATED]->(donation:Donation {{amount: '{amount}'}}) "
            # Delete that donation
            cypher += f"SET donation.amount = '{new_amount}' "
            # Run the cypher
            self.driver.session().run(cypher)

    def change_donor_name(self, firstname, lastname, new_first, new_last):
        # Get the person
        cypher = f"MATCH (p:Person {{first_name:'{firstname}', last_name:'{lastname}'}}) "
        # Then set the new name
        cypher += f"SET p.first_name = '{new_first}' "
        cypher += f"SET p.last_name = '{new_last}' "
        # Run the cypher
        self.driver.session().run(cypher)
