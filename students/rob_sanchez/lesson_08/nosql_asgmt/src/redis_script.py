"""
    demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        print('\nStep 2: cache some data in Redis...')
        r.set('andy', 'andy@somewhere.com')

        log.info('Now I can read it using the key')
        email = r.get('andy')
        log.info(f'The results of r.get(\'andy\'): {email}')

        print('\nStep 3: cache more data in Redis...')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')
        print(r.get('pam'))
        print(r.get('fred'))

        print('\nStep 4: adding and pulling richer data for a SKU...')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        cover_type = r.lindex('186675', 2)
        price = r.lindex('186675', 3)
        log.info(f'Type of cover = {cover_type}')
        log.info(f'Price = {price}')

        print('\nStep 5: Adding additional customer data to the cache...')

        # Index values:
        PHONE = 0
        ZIP = 1

        # customer 1
        r.rpush('John', '425-123-1111')
        r.rpush('John', '99501')

        # customer 2
        r.rpush('Michael', '425-123-2222')
        r.rpush('Michael', '99524')

        # customer 3
        r.rpush('Kate', '425-123-3333')
        r.rpush('Kate', '85001')

        # customer 4
        r.rpush('Tom', '425-123-4444')
        r.rpush('Tom', '85055')

        # customer 5
        r.rpush('Ron', '425-123-5555')
        r.rpush('Ron', '72201')

        # customer 6
        r.rpush('Percy', '206-321-6666')
        r.rpush('Percy', '72217')

        # Retrive zip code
        print('\nStep 6: Retrieving the Zip code of a known customer...')
        zip = r.lindex('John', ZIP)
        print(f'John\'s Zip code: {zip}')

        # Retrive phone #
        print('\nStep 7: Retrieving the Zip code of a known customer...')
        phone_number = r.lindex('Kate', PHONE)
        print(f'Kate\'s phone number: {phone_number}')

    except Exception as e:
        print(f'Redis error: {e}')
