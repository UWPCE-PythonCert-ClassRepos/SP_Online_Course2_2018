"""
    clears database for testing
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