"""
module that will login to the various demonstration databases consistently
"""

import configparser
from pathlib import Path
import redis
import mailroom_utilities

log = mailroom_utilities.configure_logger(
    'default', '../logs/mailroom_login_redis_dev.log'
)
config_file = Path(
    __file__
).parent.parent.parent.parent.parent / '.config/config.ini'

config = configparser.ConfigParser()

def login_redis_cloud():
    """
    connect to redis and login
    """
    try:
        config.read(config_file)
        host = config["redis_cloud"]["host"]
        port = config["redis_cloud"]["port"]
        pw = config["redis_cloud"]["pw"]
    except Exception as e:
        print(f'error: {e}')

    log.info('Here is where we use the connect to redis.')
    try:
        r = redis.StrictRedis(
            host=host, port=port, password=pw, decode_responses=True)
    except Exception as e:
        print(f'error: {e}')

    return r

redis_client = login_redis_cloud()
log.info(f"Redis client: {redis_client}")
