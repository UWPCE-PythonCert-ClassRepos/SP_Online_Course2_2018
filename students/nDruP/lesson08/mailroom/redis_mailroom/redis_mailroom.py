"""
This module will connect to Redis cloud, initialize the cache, and perform 
functions on the cached data.
Assignment: 
Create lookup data for validation purposes using Redis. 
You will need to populate a cache,
and show how you use the Redis cache to read the data.
"""

import configparser
from pathlib import Path
import redis


config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()
lookup_file = 'lookup_list.txt'


class Redis_Mailroom_Client():

    def __init__(self):
        try:
            config.read(config_file)
            host = config["redis_cloud"]["host"]
            port = config["redis_cloud"]["port"]
            pw = config["redis_cloud"]["pw"]

        except Exception as e:
            print(f'error: {e}')

        try:
            r = redis.StrictRedis(host=host, port=port,
                                  password=pw, decode_responses=True)

        except Exception as e:
            print(f'error: {e}')

        self.r = r
        self.keys = []
        self.lookup_data = self.parse_lookup_file(lookup_file)
        self.populate_lookup_data()

    def populate_lookup_data(self):
        """
        Take list of donors, create lookup data for each of them.
        Name: Email, Phone Number, Security Question answer
        """
        for name, email, phone, sec_q in self.lookup_data:
            self.r.hmset(name, {'email': email, 'phone_num': phone,
                                'security_answ': sec_q})
            self.keys.append(name)

    def parse_lookup_file(self, path):
        lookup_list = []
        with open(path, 'r') as lookup_file:
            for line in lookup_file:
                lookup_list.append(tuple(line[:-1].split(',')))
        return lookup_list

    def create_client(self, new_name, new_email, new_num, new_sec_answ):
        self.r.hmset(new_name, {'email': new_email, 'phone_num': new_num,
                                'security_answ': new_sec_answ})
        self.keys.append(new_name)

    def write_lookup_file(self, path):
        with open(path+'~', 'w+') as lookup_file:
            for n in self.keys:
                n_dict = self.r.hgetall(n)
                lookup_file.write(n + ',' + n_dict['email'] + ',' +
                                  n_dict['phone_num'] + ',' +
                                  n_dict['security_answ'] + '\n')

    def lookup_factory(field):
        def lookup_field(self, n):
            return self.r.hget(n, field)
        return lookup_field

    def validate_factory(field):
        def validate_field(self, name, check_field):
            r_field = self.r.hget(name, field)
            return r_field == check_field
        return validate_field

    validate_email = validate_factory('email')
    
    validate_phone_num = validate_factory('phone_num')
    
    validate_security_q = validate_factory('security_answ')

    lookup_email = lookup_factory('email')

    lookup_phone_num = lookup_factory('phone_num')
    
    lookup_security_q = lookup_factory('security_answ')
