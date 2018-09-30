"""Self-contained redis example."""

import configparser
from pathlib import Path
import redis

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

        print("\nStep 4: Delete 'andy' from cache")
        r.delete('andy')

        print('\nStep 5: Make a unique ID and use it to count.')
        r.set('user_count', 21)
        r.incr('user_count')
        r.incr('user_count')
        r.decr('user_count')
        result = r.get('user_count')
        print(f'user_count=21+1+1-1={result}')

        print('\nStep 6: Make richer data for a SKU')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        print('\nStep 7: Pull some data from the SKU structure')
        cover_type = r.lindex('186675', 2)
        print(f'Type of cover = {cover_type}')

        print('\nStep 8: Add customer data for 6 customers')
        PHONE_IDX = 0
        ZIP_IDX = 1
        customer_data = {
            'apple': {
                'phone': '012-345-6789',
                'zip': '01234'
            },
            'lucky': {
                'phone': '503-832-2833',
                'zip': '53098'
            },
            'zeke': {
                'phone': '555-555-5555',
                'zip': '98000'
            },
            'blake': {
                'phone': '838-608-0199',
                'zip': '12011'
            },
            'naomi': {
                'phone': '721-608-8223',
                'zip': '24587'
            },
            'kale': {
                'phone': '444-385-9115',
                'zip': '62214'
            },
        }
        for customer, data in customer_data.items():
            print(f"Inserting {customer}: [phone: {data['phone']}"
                  f", zip: {data['zip']}]")
            r.rpush(customer, data['phone'])
            r.rpush(customer, data['zip'])

        print('\nStep 9. Retrieve zip and phone for blake')
        blake_phone = r.lindex('blake', PHONE_IDX)
        blake_zip = r.lindex('blake', ZIP_IDX)
        print(f"Blake's info: [phone: {blake_phone}, zip: {blake_zip}]")

        print('\nFinally: Delete all data so we can start over.')
        r.flushdb()

    except Exception as e:
        print(f'Redis error: {e}')


if __name__ == '__main__':
    run_redis_example()
