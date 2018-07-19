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
import utilities

log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


class RedisMailroomClient():

    def __init__():
        try:
            config.read(config_file)
            host = config["redis_cloud"]["host"]
            port = config["redis_cloud"]["port"]
            pw = config["redis_cloud"]["pw"]

        except Exception as e:
            print(f'error: {e}')

        log.info('Here is where we use the connect to redis.')

        try:
            r = redis.StrictRedis(host=host, port=port,
                                  password=pw, decode_responses=True)

        except Exception as e:
            print(f'error: {e}')

        self.r = r

        lookup_data = self.parse_lookup_file('lookup_list.txt')
        self.populate_lookup_data(lookup_data)

    def populate_lookup_data(self, lookup_list):
        """
        Take list of donors, create lookup data for each of them.
        Name: Email, Phone Number, Security Question answer
        """
        for name, email, phone, sec_q in lookup_list:
            self.r.hmset(name, {'email': email, 'phone_num': phone,
                                'security_answ': sec_q})

    def parse_lookup_file(self, path):
        lookup_list = []
        with (path, 'r') as lookup_file:
            for line in lookup_file:
                lookup_list.append(tuple(line[:-1].split(',')))
        return lookup_list

    def validate_factory(self, field):
        def validate_field(self, name, check_field):
            r_field = self.r.hget(name, field)
            return r_field == check_field
        return validate_field

    validate_email = validate_factory('email')
    
    validate_phone_num = validate_factory('phone_num')
    
    validate_security_q = validate_factory('security_answ')
