"""
Main classes of the mailroom.
"""

import login_database
import utilities
import pymongo
import donors

log = utilities.configure_logger('default', '../logs/mongo.log')

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
        with login_database.login_mongodb_cloud() as client:
            self.db = client['mailroom']
            self.donors = self.db['donors']

            # Drop DB and start fresh
            log.info('Dropping DB')
            self.db.drop_collection('donors')
            self.populate_db()

    def populate_db(self):
        """ Populates DB with sample data. """
        # Get donors
        log.info("Populating DB with sample data.")
        donor_info = donors.get_donors()
        try:
            self.donors.insert_many(donor_info)
            log.info("Database populated.")

        except Exception as e:
            log.error(f"Database NOT populated {e}")

    def get_donor(self):
        return input("Enter a donor: ")

    def get_donation(self):
        return int(input("Enter a donation amount: "))

    def add_donation(self):
        """ Adds a donation to an existing donor.  Otherwise adds a new donor. """
        input_donor = self.get_donor().title()
        input_donation = self.get_donation()

        # Check for existing donor.  Update if found.
        for donor in self.donors.find():
            if donor['name'].title() == input_donor:
                log.info("Updating donation totals.")
                previous_total = int(donor['donations'])
                new_total = previous_total + input_donation
                
                log.info("Updating count and average.")
                count = int(donor['count'])
                new_count = count + 1
                new_average = new_total / new_count

                log.info("Updating donor amount.")
                self.donors.update_one(
                    {
                        'name': input_donor
                    },
                    {
                        '$set':
                        {
                            'name': input_donor,
                            'donations': new_total,
                            'average': new_average,
                            'count': new_count
                        }
                    }
                )
                log.info("Donor updated")
                break

            # New donor insert
            else:
                log.info("Adding new donor.")
                self.donors.insert_one({
                    'name': input_donor,
                    'donations': input_donation,
                    'average': input_donation,
                    'count': '1'
                })
                break

    def update_donor(self):
        """ Updates a donor's name. """
        input_donor = self.get_donor()
        input_donor = input_donor.title()
        input_name = input("Please enter a new name: ")
        input_name = input_name.title()

        for donor in self.donors.find():
            if donor['name'] == input_donor:
                log.info("Updating donor name.")
                self.donors.update_one(
                    {
                        'name': input_donor
                    },
                    {
                        '$set':
                        {
                            'name': input_name,
                            'donations': donor['donations'],
                            'average': donor['average'],
                            'count': donor['count']
                        }
                    }
                )
                log.info("Donor updated.")
                break

    def delete_donor(self):
        """ Deletes a donor. """
        input_donor = self.get_donor()
        input_donor = input_donor.title()

        for donor in self.donors.find():
            if donor['name'] == input_donor:
                log.info("Deleting donor.")
                self.donors.delete_many(
                    {'name': input_donor}
                )
                log.info("Donor deleted.")
                break

    def create_report(self):
        """ Creates a formatted donor report. """
        # Base setup
        line_out = ''
        line_out += "Donor:                    | $    Total     |\
           Donations   | $   Average   |\n"
        line_out += ("-"*76) + '\n'
        print(line_out)

        for donor in self.donors.find():
            print('{:<26}| ${:>14,.2f}|{:>15}| ${:>13,.2f}'.format(donor['name'], float(donor['donations']), donor['count'], float(donor['average'])))
        
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
        if test_flag:
            for donor in self.donors.find():
                print(letter.format(donor['name'], donor['donations']))
        else:
            for donor in self.donors.find():
                with open(f"{donor['name']}_letter.txt", 'w+') as outfile:
                    outfile.write(letter.format(donor['name'], donor['donations']))
    
    @property
    def all_donors(self):
        """ Class property list of all names. """
        return [donor['name'] for donor in self.donors.find()]

    def list_donors(self):
        """ Prints all donors. """
        for name in self.all_donors: print(name)
    
    @property
    def all_donors_and_donations(self):
        """ Class property dict of all names and their donations. """
        all_info = []
        for donor in self.donors.find():
            all_info.append(
                {
                    'name': donor['name'],
                    'donations': donor['donations'],
                    'average': donor['average'],
                    'count': donor['count']
                }
            )
        return all_info

    
        
        