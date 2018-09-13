"""
Main classes of the mailroom.
"""

import login_database
import utilities
import pymongo
import donors

log = utilities.configure_logger('default', '../logs/redis.log')

class Mailroom:
    """
    Features: lookup data for validation
    """

    def __init__(self):
        try:
            self.r = login_database.login_redis_cloud()
            self.r.flushdb()
            self.populate_db()
        except Exception as e:
            print(f"Redis error: {e}")

    def populate_db(self):
        """
        Populates DB with sample data. Couldn't get the hash map to work
        just passing it in.
        """
        # Get donors
        log.info("Populating donors.")

        self.r.hmset('Thomas', {'donations': '500', 'email': 'thomas@thomas.com', 'city': 'Athens', 'state': 'GA', 'zip': 30606})

        self.r.hmset('Ted', {'donations': '1', 'email': 'ted@ted.com', 'city': 'Memphis', 'state': 'TN', 'zip': 38104})

        self.r.hmset("Bailey", {'donations': '1000', 'email': 'bailey@bailey.com', 'city': 'Washington', 'state': 'DC', 'zip': 12345})

    def get_donor(self):
        return input("Enter a donor: ").title()

    def get_donor_info(self):
        """ Returns all info about 1 donor. """
        name = self.get_donor()
        if name in self.all_donors:
            person = self.r.hgetall(name)
            print(f"Person: {name}")
            for key, value in person.items():
                print(f"{key}: {value}")
        else:
            print("Name not in database.")

    def add_donation(self):
        """ Adds a donation and/or donor. """
        name = self.get_donor()
        # Update existing
        if name in self.all_donors:
            input_donation = int(input("Please enter a donation: "))
            donations = int(self.r.hget(name, 'donations'))
            donations += input_donation

            self.r.hset(name, 'donations', str(donations))
            print(self.r.hget(name, 'donations'))
        # Create new
        else:
            print("New donor found.  Please enter the following information: ")
            input_donation = str(input("Please enter a donation: "))  # should add value error checking by going from str to int to str
            input_email = input("Please enter an email: ")
            input_city = input("Please enter a city: ")
            input_state = input("Please enter a state: ")
            input_zip = input("Please enter the zipcode: ")
            self.r.hmset(name, {'donations': input_donation, 'email':input_email, 'city': input_city, 'state': input_state, 'zip': input_zip})

    def get_donor_email(self):
        """ Returns email from 1 donor. """
        input_name = self.get_donor()
        if input_name in self.all_donors:
            print(self.r.hget(input_name, 'email'))

    def create_report(self):
        """ Creates a formatted report with donor, donations, and email. """
        # Base setup
        line_out = ''
        line_out += "{:<15} | {:^15} | {:^30}\n".format("Name", "Donations", "Email")
        line_out += ("-"*65)
        print(line_out)

        # Setup line format to recieve ordered donor info 
        for name in self.all_donors:
            line = "{:<15} | {:^15} | {:^30}".format(name, self.r.hget(name, 'donations'), self.r.hget(name, 'email'))
            print(line)

    def delete_donor(self):
        input_name = self.get_donor()
        if input_name in self.all_donors:
            self.r.delete(input_name)

    @property
    def all_donors(self):
        """ Class property list of all names. """
        return [item for item in self.r.keys()]

    def list_donors(self):
        """ Prints all donors. """
        for item in self.all_donors: print(item)

    def all_donors_all_donation(self):
        """ Class property of all donors and donation. """
        for name in self.all_donors:
            person = self.r.hgetall(name)
            print(f"Person: {name}")
            for key, value in person.items():
                print(f"{key}: {value}")



