import login_database as login_database
import utilities as utilities

def get_people_data():
    """
    Create some people for the mailroom MongoDB database.
    """

    people_data = [
        {
            'donor': 'Shane',
            'donations': [6, 5, 10],
        },
        {
            'donor': 'Pete',
            'donations': [7,8],
        },
        {
            'donor': 'Zach',
            'donations': [10],
        },
        {
            'donor': 'Fitz',
            'donations': [1],
        },
        {
            'donor': 'Joe',
            'donations': [5, 4, 3, 2, 1],
        }

    ]
    return people_data


def populate_redis(r):
    """Create a cache of data for Lesson 08 mailroom"""
    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        # login_database.login_redis_cloud()
        log.info('For Lesson 08 Assignment, add name, tele, and email.')
        # first delete the key if it exists already
        r.delete('Shane')
        # then create a new entry
        r.rpush('Shane', 'Repking')
        r.rpush('Shane', '677-0180')
        r.rpush('Shane', 'sr@gmail.com')

        # first delete the key if it exists already
        r.delete('Zach')
        r.rpush('Zach', 'Gillis')
        r.rpush('Zach', '677-0181')
        r.rpush('Zach', 'zg@gmail.com')

        # first delete the key if it exists already
        r.delete('Joe')
        r.rpush('Joe', 'Slinger')
        r.rpush('Joe', '677-0182')
        r.rpush('Joe', 'js@gmail.com')

        # first delete the key if it exists already
        r.delete('Fitz')
        r.rpush('Fitz', 'Patrick')
        r.rpush('Fitz', '677-0183')
        r.rpush('Fitz', 'fp@gmail.com')

        # first delete the key if it exists already
        r.delete('Pete')
        r.rpush('Pete', 'Chair')
        r.rpush('Pete', '876-9546')
        r.rpush('Pete', 'pc@gmail.com')



    except Exception as e:
        print(f'Redis error: {e}')
