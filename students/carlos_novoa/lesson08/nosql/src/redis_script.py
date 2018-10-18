"""
    Redis
"""


import login_database
import utilities


def run_example():
    """
    Refactored Redis example
    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        r = login_database.login_redis_cloud()

        log.info(f'Add more customer data')
        customers = [
            ['halpert', {'telephone': '111-111-1111', 'zip': '11111'}],
            ['michael', {'telephone': '222-222-2222', 'zip': '22222'}],
            ['kevin', {'telephone': '333-333-3333', 'zip': '33333'}],
            ['oscar', {'telephone': '444-444-4444', 'zip': '44444'}],
            ['ryan', {'telephone': '555-555-5555', 'zip': '55555'}],
            ['Phyllis', {'telephone': '666-666-6666', 'zip': '66666'}]
        ]

        for key, data in customers:
            r.hmset(key, data)

        log.info(f'Retreive customer info')
        key = "oscar"
        result = r.hgetall(key)
        print(f"Telephone for {key}: {result['telephone']}")
        print(f"Zip for {key}: {result['zip']}")

    except Exception as e:
        print(f'Redis error: {e}')
