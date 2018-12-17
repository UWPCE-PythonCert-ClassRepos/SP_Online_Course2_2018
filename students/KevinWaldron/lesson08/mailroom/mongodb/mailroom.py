#!/usr/bin/env python3

import logging
import configparser
import pymongo

from pathlib import Path
from operator import itemgetter

class Donor():
    logger = logging.getLogger(__name__)

    """
    An individual donor, consisting of a name the wraps the IndividualDonor and Donations database tables
    """
    def __init__(self, name, db):
        self._name = name
        self._db = db
        self._donor_collection = db['donors']
        self._donations_collection = db['donations']

    @property
    def total_donations(self):
        return self._donor_collection.find_one({"name": self._name})['total_donations']

    @property
    def name(self):
        return self._name

    @property
    def avg_donation(self):
        return self._donor_collection.find_one({"name": self._name})['average_donation']

    @property
    def num_donations(self):
        return self._donations_collection.count_documents({'name': self._name})

    def add_donation(self, donation):
        """
        Add a new donation entry for this donor to the database
        :param donation: the new donation amount
        """
        try:
            self._donor_collection.find_one({"name": self._name})['total_donations']

            new_donation = {
                'name': self.name,
                'amount': donation}
            self._donations_collection.insert_one(new_donation)
            donor = self._donor_collection.find_one({"name": self._name})
            donor['total_donations'] = donor['total_donations'] + donation
            donor['average_donation'] = donor['total_donations'] / self.num_donations
            self._donor_collection.find_one_and_update({"_id": donor['_id']}, {"$set": {"total_donations": donor['total_donations'], "average_donation": donor['average_donation']}})
        except Exception as e:
            logger.error(f"Failed to add donation {donation} for {self._name}", e)

    def create_thank_you(self, donation):
        """
        Prints a thank for you the given donor and amount
        :param donation: dictionary containing name of the donor to thank and the amount donated
        :returns: formatted thank you string
        """
        return f"Dear {self.name},\nThank you for your very generous donation of ${donation:.2f}.  It \nwill go very far in supporting the Human Fund, \"Money for \nPeople.\"\n{'Sincerely':>40}\n{'Art Vandelay':>50}"

    def list_donations(self):
        """
        List donations by this donor
        """
        query = self._donations_collection.find({"name": self._name})
        return f"\n{'-'*10} Donations by {self._name} {'-'*10}\n" + '\n'.join(["{:.2f}".format(donation['amount']) for donation in query])

    def __lt__(self, other):
        return self.total_donations < other.total_donations

    def __eq__(self, other):
        return self.name == other.name

class Donors():
    logger = logging.getLogger(__name__)

    """
    A collection of donors
    """
    def __init__(self, db):
        self._donors = []
        self._db = db
        self._donor_collection = db['donors']
        self._donations_collection = db['donations']

        for donor in self._donor_collection.find():
            self._donors.append(Donor(donor['name'], db))

    def add_donor(self, donor):
        """
        Add a new donor to the donors list
        :param donor: the new donor to add
        """
        self._donors.append(donor)

    def list_donors(self):
        """ Creates a list of the donors by name """
        return f"\n{'-'*10} Donors {'-'*10}\n" + '\n'.join([donor.name for donor in self._donors])

    def print_donors(self):
        """ Prints the list of donors """
        print(self.list_donors())

    def find_donor(self, name):
        """
        Find a donor by name
        :param name: the name of the donor to search for
        :return: The donor if found else None
        """
        for donor in self._donors:
            if donor.name == name:
                return donor
        return None

    def add_donation(self, name, amount):
        """
        Add a donation.
        :param name: the name of the donor.
        :param amount: the amount of the donation.the
        :returns: the list of donations for the donor
        """
        donor = self.find_donor(name)
        if donor is None:
            donor = Donor(name, self._db)
            try:
                new_donor = {
                    'name': name,
                    'total_donations': 0.0,
                    'average_donation': 0.0}
                self._donor_collection.insert_one(new_donor)
                self.add_donor(donor)
            except Exception as e:
                logger.error(f"Failed to add new donor {name} to database", e)
        amount = float(amount)
        donor.add_donation(amount)
        print("\n" + donor.create_thank_you(amount))
        return donor

    def create_report(self):
        """
        Handles the create report menu selection
        :returns: returns the report string
        """
        header = "\n{:<20}| Total Given | Num Gifts | Average Gift\n".format("Donor Name")
        result = header
        result += f"{'-' * (len(header) - 1)}"

        sorted_donors = sorted(self._donor_collection.find(), key=itemgetter('total_donations'), reverse=True)
        for donor in sorted_donors:
            result += "\n{:<20}| ${:>10.2f} | {:>9} | ${:>11.2f}".format(donor['name'], donor['total_donations'], self._donations_collection.count_documents({'name': donor['name']}), donor['average_donation'])
        return result

    def print_report(self):
        """ Prints the report """
        print(self.create_report())

    def mail_everyone(self):
        """ Handles the mail to everyone menu selection """
        for donor in self._donors:
            with open(donor.name.lower().replace(' ', "_") + ".txt", 'w') as f:
                f.write(donor.create_thank_you(donor.total_donations))

    def delete_donor(self, name):
        """ Deletes a donor and all donation records """
        donor = self.find_donor(name)
        self._donors.remove(donor)
        self._donor_collection.remove({"name": {"$eq": name}})
        self._donations_collection.remove({'name': {'$eq': name}})

class Mailroom:
    def __init__(self, db):
        self._donors = Donors(db)
        self._db = db

    @property
    def donors_list(self):
        return self._donors

    def quit_menu(self):
        """ Handles the menu quit selection """
        return "Quit"

    def donation_entry(self, name):
        """
        Handles the donation entry and prints the thank you to the screen.
        :param name: the name of the donor
        """
        amount = input("Enter donation amount or 'q' to return to the main menu: ")
        if (amount == "q"):
            return
        try:
            self._donors.add_donation(name, amount)
        except ValueError:
            print("Please enter a valid number.")
            self.donation_entry(name)

    def donor_entry(self):
        """ Handles donor entry menu selection """
        name = input("\nEnter donor's full name or 'q' to return to the previous menu: ")
        if(name == "q"):
            return
        self.donation_entry(name)

    def delete_donor(self):
        """ Handles donor deletion """
        name = input("\nEnter donor's full name to delete or 'q' to return to the previous menu: ")
        if(name == "q"):
            return
        if self._donors.find_donor(name) is None:
            print("No donor by that name, please try again")
            self.delete_donor()
        else:
            self._donors.delete_donor(name)

    def list_donations(self):
        """ Handles donor donations list """
        name = input("\nEnter donor's full name for a list of donations or 'q' to return to the previous menu: ")
        if(name == "q"):
            return
        donor = self._donors.find_donor(name)
        if donor is None:
            print("No donor by that name, please try again")
            self.list_donations()
        else:
            print(donor.list_donations())

    def send_thank_you(self):
        """ Handles the send thank you menu selection """
        # modify donor entry slightly (no more list) to reuse display prompt funtion
        thank_you_menu_prompt = "1. Enter donation\n2. See a list of donors\n3. Return to previous menu"
        thank_you_menu_dict = {'1':self.donor_entry, '2':self._donors.print_donors, '3':self.quit_menu}
        self.display_prompt(thank_you_menu_prompt, thank_you_menu_dict)

    def display_prompt(self, menu_prompt, menu_dict):
        """
        Handles the user input loop for a menu of options by displaying the menu prompt and dispatching
        to the appropriate method based on the user selection

        :param menu_prompt: the menu prompt
        :param menu_dict: the mapping of menu selections to functions
        """
        while True :
            print("\nChoose from the following menu of options:")
            print(menu_prompt)
            selection = input("\nPlease enter your choice: ")
            try:
                if menu_dict[selection]() == "Quit":
                    break
            except KeyError:
                print("Invalid selection")

config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()

def login_mongodb_cloud():
    """
        connect to mongodb and login
    """
    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]
    except Exception as e:
        print(f'error: {e} {config_file}')

    client = pymongo.MongoClient(f'mongodb://{user}:{pw}'
                                 '@cluster0-shard-00-00-wcehp.mongodb.net:27017,'
                                 'cluster0-shard-00-01-wcehp.mongodb.net:27017,'
                                 'cluster0-shard-00-02-wcehp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')

    return client

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    logger = logging.getLogger(__name__)

    client = login_mongodb_cloud()
    db = client['mailroom']

    mailroom = Mailroom(db)
    main_menu_prompt = "1. Send a Thank You\n2. Create a Report\n3. Send letters to everyone\n4. Delete Donor\n5. List Donations\n6. Quit"
    main_menu_dict = {'1': mailroom.send_thank_you, '2':mailroom.donors_list.print_report, '3':mailroom.donors_list.mail_everyone, '4':mailroom.delete_donor, '5':mailroom.list_donations, '6':mailroom.quit_menu}
    mailroom.display_prompt(main_menu_prompt, main_menu_dict)