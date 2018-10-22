import configparser
from pathlib import Path
import redis


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


def login_redis_cloud():
    """
        connect to redis and login
    """
    config_file = Path(__file__).parent / '.config/config.ini'
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        host = config["redis_cloud"]["host"]
        port = config["redis_cloud"]["port"]
        pw = config["redis_cloud"]["pw"]


    except Exception as e:
        print(f'error: {e}')

    try:
        r = redis.StrictRedis(host=host, port=port, password=pw, decode_responses=True)

    except Exception as e:
        print(f'error: {e}')

    return r


class DonorCollection:
    """
        Encapsulates the db. Gets data from it
        and returns the data as a Donor. Inserts data
        when necessary.
    """

    def __init__(self):
        self.redis = login_redis_cloud()

    def get_donors(self):
        # Get the list of donors
        all_donors = self.redis.scan_iter()

        # Iterate over each donor
        for d in all_donors:
            # Convert this donors donations to a list
            donation_len = self.redis.llen(d)
            all_donations = list()
            for donation in self.redis.lrange(d, 0, donation_len):
                all_donations.append(float(donation))

            # Split up the name for convenience
            len = int(all_donations[0])
            first_name = d[:len]
            last_name = d[len:]
            yield Donor(first_name, last_name, all_donations[1:])

    def add_donation(self, firstname, lastname, amount):
        name = firstname + lastname
        index = len(firstname)
        if self.redis.llen(name) == 0:
            self.redis.rpush(name, index)
        self.redis.rpush(name, amount)

    def delete_donor(self, firstname, lastname):
        self.redis.delete(firstname + lastname)

    def get_donations(self, firstname, lastname):
        name = firstname + lastname
        donation_len = self.redis.llen(name)
        donations_list = list()
        for donation in self.redis.lrange(name, 1, donation_len):
            donations_list.append(float(donation))
        return donations_list

    def delete_donation(self, firstname, lastname, delete_num):
        name = firstname + lastname
        delete_val = self.redis.lindex(name, delete_num + 1)
        self.redis.lrem(name, 1, delete_val)

    def change_donation(self, firstname, lastname, change_num, new_amount):
        name = firstname + lastname
        self.redis.lset(name, change_num + 1, new_amount)

    def change_donor_name(self, firstname, lastname, new_first, new_last):
        old_name = firstname + lastname
        new_name = new_first + new_last
        self.redis.rename(old_name, new_name)
        name_len = len(new_first)
        self.redis.lset(new_name, 0, name_len)
