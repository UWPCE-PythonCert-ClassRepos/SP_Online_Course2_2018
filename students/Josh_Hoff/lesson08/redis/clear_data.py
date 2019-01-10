"""
    clears database for testing
    WARNING: THIS WILL CLEAR ALL KEYS IN THE REDIS DATABASE
"""

import login_redis

def clear_database():
    """
        redis data removal
    """
    try:
        r = login_redis.login_redis_cloud()
        r.flushall()

    except Exception as e:
        print(f'Redis error: {e}')

if __name__ == '__main__':
    clear_database()