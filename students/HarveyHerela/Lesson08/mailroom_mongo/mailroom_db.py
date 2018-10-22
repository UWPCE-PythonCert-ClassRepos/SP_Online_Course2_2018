import configparser
from pathlib import Path
import pymongo


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


def login_mongodb_cloud():
    """
        connect to mongodb and login
    """

    try:
        config_file = Path(__file__).parent / '.config/config.ini'
        config = configparser.ConfigParser()
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]

    except Exception as e:
        print(f'error: {e}')

    client = pymongo.MongoClient(f'mongodb://{user}:{pw}'
                                 '@cluster0-shard-00-00-m7w80.mongodb.net:27017,'
                                 'cluster0-shard-00-01-m7w80.mongodb.net:27017,'
                                 'cluster0-shard-00-02-m7w80.mongodb.net:27017/test'
                                 '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')

    return client

class DonorCollection:
    """
        Encapsulates the db. Gets data from it
        and returns the data as a Donor. Inserts data
        when necessary.
    """
    def __init__(self):
        client = login_mongodb_cloud()
        db = client.mailroom
        self.donors = db.donors
        self.donations = db.donations

    def get_donors(self):
        # Iterate over each donor
        for d in self.donors.find():
            # Get all of this donors donations, and save it as a list
            query = {'donor_id': d['_id']}
            all_donations = list()
            for donation in self.donations.find(query):
                all_donations.append(donation['amount'])

            yield Donor(d['firstname'], d['lastname'], all_donations)

    def add_donation(self, firstname, lastname, amount):
        name = firstname + lastname
        query = {'name': name}
        donor_result = self.donors.find_one(query)
        donor_id = None

        # If the donor doesn't exist, add the donor to the database
        if donor_result == None:
            insert_result = self.donors.insert_one({'name': name, 'firstname': firstname, 'lastname': lastname})
            donor_id = insert_result.inserted_id
        else:
            donor_id = donor_result['_id']

        # Add the donation
        self.donations.insert_one({'donor_id':donor_id, 'amount': amount})

    def delete_donor(self, firstname, lastname):
        # Get the donor id
        query = {'name': firstname + lastname}
        donor = self.donors.find_one(query)
        donor_id = donor['_id']

        # Delete the donor
        self.donors.delete_one(query)

        # Delete all donations by this donor
        del_query = {'donor_id': donor_id}
        self.donations.delete_many(del_query)

    def get_donations(self, firstname, lastname):
        # Get the donor id
        query = {'name': firstname + lastname}
        donor = self.donors.find_one(query)
        donor_id = donor['_id']

        query = {'donor_id': donor_id}
        all_donations = list()
        for donation in self.donations.find(query):
            all_donations.append(donation['amount'])

        return all_donations

    def delete_donation(self, firstname, lastname, delete_num):
        # Get the donor id
        query = {'name': firstname + lastname}
        donor = self.donors.find_one(query)
        donor_id = donor['_id']

        query = {'donor_id': donor_id}
        all_donations = list()
        for donation in self.donations.find(query):
            all_donations.append(donation['amount'])

        amount = all_donations[delete_num]
        del_query = {'donor_id': donor_id, 'amount': amount}
        self.donations.delete_one(del_query)

    def change_donation(self, firstname, lastname, change_num, new_amount):
        # Get the donor id
        query = {'name': firstname + lastname}
        donor = self.donors.find_one(query)
        donor_id = donor['_id']

        query = {'donor_id': donor_id}
        all_donations = list()
        for donation in self.donations.find(query):
            all_donations.append(donation['amount'])

        amount = all_donations[change_num]
        query = {'donor_id': donor_id, 'amount': amount}
        up_query = {'$set':
            {'amount': new_amount}
        }
        self.donations.update_one(query, up_query)

    def change_donor_name(self, firstname, lastname, new_first, new_last):
        query = {'name': firstname + lastname}
        update = {'$set':
            {
                'name': new_first + new_last, 'firstname': new_first, 'lastname': new_last
            }
        }
        self.donors.update_one(query, update)
