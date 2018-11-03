"""
    demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-persistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.set('test', 'test@testing.net')

        log.info('Step 2: adding some data to cache')
        r.hmset('Keith', {'phone': '425-123-4567', 'zip code': '91234'})
        r.hmset('Allison', {'phone': '206-987-6543', 'zip code': '94321'})
        r.hmset('Jesse', {'phone': '360-123-4567', 'zip code': '90101'})
        r.hmset('Lauren', {'phone': '425-606-6060', 'zip code': '96060'})
        r.hmset('John', {'phone': '206-206-2062', 'zip code': '92062'})
        r.hmset('Merlin', {'phone': '800-900-1000', 'zip code': '87654'})

        log.info('Step 3: return Merlin\'s zip code.')
        merlin_zip = r.hmget('Merlin', 'zip code')
        log.info(f'Merlin\'s zip code: {merlin_zip}')

        log.info('Step 4: return Merlin\'s phone number.')
        merlin_phone = r.hmget('Merlin', 'phone number')
        log.info(f'Merlin\'s phone number: {merlin_phone}')

    except Exception as e:
        print(f'Redis error: {e}')
