"""Self-contained redis example."""

import configparser
from pathlib import Path
#import pprint
import redis
#import seed_data

config_file = Path(__file__).parent / '.config/config.ini'
config = configparser.ConfigParser()

def login_redis_cloud():
    """Connect to redis and login."""

    try:
        config.read(config_file)
        host = config["redis_cloud"]["host"]
        port = config["redis_cloud"]["port"]
        pw = config["redis_cloud"]["pw"]
        print(f'Got host={host} port={port} pw=***** from {config_file}')
    except Exception as e:
        print(f'Error parsing {config_file}: {e}')

    try:
        r = redis.StrictRedis(host=host, port=port, password=pw,
                              decode_responses=True)
    except Exception as e:
        print(f'Error connecting to Redis DB: {e}')

    return r


def run_redis_example():
    """Redis example from course, extended as needed for lesson08."""

    try:
        print('\nStep 1: Connect to Redis')
        r = login_redis_cloud()
        print('\nStep 2: Cache some data in Redis and read it back')
        r.set('andy', 'andy@somewhere.com')
        email = r.get('andy')
        print(f"r.get('andy'): {email}")

        print('\nStep 3: Cache more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

        print("Step 4: Delete 'andy' from cache")
        r.delete('andy')

        print('Step 5: Make a unique ID and use it to count.')
        r.set('user_count', 21)
        r.incr('user_count')
        r.incr('user_count')
        r.decr('user_count')
        result = r.get('user_count')
        print(f'user_count=21+1+1-1={result}')

        print('Step 6: Make richer data for a SKU')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        print('Step 7: Pull some data from the SKU structure')
        cover_type = r.lindex('186675', 2)
        print(f'Type of cover = {cover_type}')

    except Exception as e:
        print(f'Redis error: {e}')


if __name__ == '__main__':
    run_redis_example()
