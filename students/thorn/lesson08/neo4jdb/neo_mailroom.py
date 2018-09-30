"""
Main classes of the mailroom.
"""

import login_database
import utilities
import pymongo
import donors


log = utilities.configure_logger('default', '../logs/neo.log')

class Mailroom:
    def __init__(self):
        self.driver = login_database.login_neo4j_cloud()

    def populate_db(self):
        """ Populates DB with sample data. """
        # Get donors
        try:
            with self.driver.session() as session:
                # Clear db before adding more data
                session.run("MATCH (n) DETACH DELETE n")
                session.run("create (n:Person {name: 'Tom H', donation: [100]})")
                session.run("create (n:Person {name: 'Ted H', donation: [200, 300]})")
                session.run("create (n:Person {name: 'Bailey K', donation: [678.99]})")

        except Exception as e:
            log.error(f"Database NOT populated {e}")

    def get_donor(self):
        return input("Enter a donor: ")

    def get_donation(self):
        return float(input("Enter a donation amount: "))

    def add_donation(self):
        """ Adds a donation to an existing donor.  Otherwise adds a new donor. """
        input_donor = self.get_donor().title()
        input_donation = self.get_donation()
        
        with self.driver.session() as session:
            # Check for existing donor.  Update if found.
            if input_donor in self.all_donors:
                donor_info = session.run("MATCH (n:Person) RETURN n.name as name, n.donation as donation")
                for donor in donor_info:
                    if input_donor == donor['name']:
                        donations = donor['donation']
                        print("Current amount: ", donations)
                        donations.append(input_donation)
                        print("Amount to add: ", donations)
                        
                        # Match on name and set new donation list
                        session.run("MATCH (n:Person {name:'%s'}) SET n.donation = %a)" % (input_donor, donations)
            # New donor insert
            else:
                print("Donor not found. Adding to database.")
                session.run("CREATE (n:Person {name:' %s', donation: '%s'})") % (input_donor, input_donation)


    def delete_donor(self):
        """ Deletes a donor. """
        input_donor = self.get_donor()
        input_donor = input_donor.title()

        with self.driver.session() as session:
            if input_donor in self.all_donors:
                target = "MATCH (n:Person {name:'%s'}) DELETE n" % (input_donor)
                session.run(target)
                print(f"{input_donor} has been deleted.")

    def create_report(self):
        """ Creates a formatted donor report. """
        # Base setup
        line_out = ''
        line_out += "{:<15} | {:^15} | {:^15} | {:^15}\n".format("Name", "Donations", "# Donations", "Average")
        line_out += ("-"*76) + '\n'
        print(line_out)
        
        # Create stats
        with self.driver.session() as session:
            donors = session.run("MATCH (n:Person) return n.name as name, n.donation as donation")
            for donor in donors:
                name = donor[0]
                donations = donor[1]
                num_donations = len(donor[1])
                sum_donations = sum(float(donation) for donation in donor[1])
                avg_donation = sum_donations / num_donations

                print("{:<15} | {:^15} | {:^15} | {:^15}".format(name, sum_donations, num_donations, avg_donation))

        
    def send_letters(self, test_flag=True):
        """ 
        Writes letters.  
        CURRENTLY ONLY PRINTS (to prevent deleting them over and over). """
        letter =\
        """
        Dear {},
        Thank you for your generous donations of {}.
                                    Sincerely,
                                    The Team
        """
        with self.driver.session() as session:
            donors = session.run("MATCH (n:Person) return n.name as name, n.donation as donation")

            for donor in donors:
                name = donor[0]
                sum_donations = sum(float(donation) for donation in donor[1])
                print(letter.format(name, sum_donations))
            
                if not test_flag:
                    with open(f'{name}_thanks.txt', 'w+') as outfile:
                        outfile.write(letter.format(name, sum_donations))

    @property
    def all_donors(self):
        """ Class property list of all names. """
        with self.driver.session() as session:
            donors = session.run("MATCH (n:Person) return n.name")
        return [donor[0] for donor in donors]

    def list_donors(self):
        """ Prints all donors. """
        for donor in self.all_donors:
            print(donor)

    def all_donors_and_donations(self):
        """ Class property dict of all names and their donations. """
        with self.driver.session() as session:
            donor_info = session.run("MATCH (n:Person) return n.name as name, n.donation as donation")
        for info in donor_info:
            print(f"{info['name']} has donated {info['donation']}")

    
        
        