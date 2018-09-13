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
    Features:
      - Add
      - Update
      - Delete
      - Show specific donor info
      - Show all donor info
    """

    def __init__(self):
        try:
            self.r = login_database.login_redis_cloud()
            self.r.flushdb()
        except Exception as e:
            print(f"Redis error: {e}")

    def populate_db(self):
        """
        Populates DB with sample data. Couldn't get the hash map to work
        just passing it in.
        """
        # Get donors
        log.info("Populating donors.")

        self.r.hmset('Thomas', {'donations': '500', 'email': 'thomas@thomas.com', 'city': 'Athens', 'state': 'GA', 'zip': '30606'})

        self.r.hmset('Ted', {'donations': '1', 'email': 'ted@ted.com', 'city': 'Memphis', 'state': 'TN', 'zip': '38104'})

        self.r.hmset("Bailey", {'donations': '1000', 'email': 'bailey@bailey.com', 'city': 'Washington', 'state': 'DC', 'zip': '12345'})

    def get_donor(self):
        return input("Enter a donor: ")

    def get_donation(self):
        return int(input("Enter a donation amount: "))

    # def add_donation(self):
    #     """ Adds a donation to an existing donor.  Otherwise adds a new donor. """
    #     input_donor = self.get_donor().title()
    #     input_donation = self.get_donation()

    #     # Check for existing donor.  Update if found.
    #     pass

    # def update_donor(self):
    #     """ Updates a donor's name. """
    #     input_donor = self.get_donor()
    #     input_donor = input_donor.title()
    #     input_name = input("Please enter a new name: ")
    #     input_name = input_name.title()

    #     pass

    # def delete_donor(self):
    #     """ Deletes a donor. """
    #     input_donor = self.get_donor()
    #     input_donor = input_donor.title()

    #     pass

    # def create_report(self):
    #     """ Creates a formatted donor report. """
    #     pass
    #     # Base setup
    #     line_out = ''
    #     line_out += "Donor:                    | $    Total     |\
    #        Donations   | $   Average   |\n"
    #     line_out += ("-"*76) + '\n'
    #     print(line_out)

    #     for donor in self.donors.find():
    #         print('{:<26}| ${:>14,.2f}|{:>15}| ${:>13,.2f}'.format()

    # def send_letters(self, test_flag=True):
    #     """
    #     Writes letters.
    #     CURRENTLY ONLY PRINTS (to prevent deleting them over and over).
    #     """
    #     pass
    #     letter =\
    #     """
    #     Dear {},
    #     Thank you for your generous donations of {}.
    #                                 Sincerely,
    #                                 The Team
    #     """
    #     if test_flag:
    #         for donor in self.donors.find():
    #             print(letter.format()
    #     else:
    #         for donor in self.donors.find():
    #             with open(f"{donor['name']}_letter.txt", 'w+') as outfile:
    #                 outfile.write(letter.format())

    @property
    def all_donors(self):
        """ Class property list of all names. """
        try:
            r = login_database.login_redis_cloud()
            return [item for item in r.keys()]
        except Exception as e:
            print("Redis error: {e}")


    def list_donors(self):
        """ Prints all donors. """
        print(self.all_donors)

    @property
    def all_donors_and_donations(self):
        """ Class property dict of all names and their donations. """
        pass



