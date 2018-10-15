"""
module that will sign in to the Redis database consistently
"""

import configparser
from pathlib import Path
import redis
import mailroom_utilities

LOG = mailroom_utilities.configure_logger(
    'default', '../logs/mailroom_login_redis_dev.log'
)
CONFIG_FILE = Path(
    __file__
).parent.parent.parent.parent.parent / '.config/config.ini'

CONFIG = configparser.ConfigParser()

def login_redis_cloud():
    """
    connect to redis and login
    """
    try:
        CONFIG.read(CONFIG_FILE)
        host = CONFIG["redis_cloud"]["host"]
        port = CONFIG["redis_cloud"]["port"]
        pw = CONFIG["redis_cloud"]["pw"]
    except Exception as e:
        print(f'error: {e}')

    LOG.info('Here is where we use the connect to redis.')
    try:
        r = redis.StrictRedis(
            host=host, port=port, password=pw, decode_responses=True)
    except Exception as e:
        print(f'error: {e}')

    return r

REDIS_CLIENT = login_redis_cloud()
LOG.info(f"Redis client: {REDIS_CLIENT}")
