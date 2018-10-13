"""
module that will login to the various demonstration databases consistently
"""

import configparser
import urllib
from pathlib import Path
import pymongo
import mailroom_utilities

log = mailroom_utilities.configure_logger(
    'default', '../logs/mailroom_login_mongodb_dev.log'
)
config_file = Path(
    __file__
).parent.parent.parent.parent.parent / '.config/config.ini'

config = configparser.ConfigParser()

def login_mongodb_cloud():
    """
    connect to mongodb and login
    """
    log.info('Here is where we use the connect to mongodb.')
    log.info('Note use of f string to embed the user & password (from the tuple).')
    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]
    except Exception as e:
        print(f'error: {e}')
    client = pymongo.MongoClient(
        urllib.parse.quote_plus(
            f'mongodb://{user}:{pw}'
            '@cluster0-shard-00-00-5pmzk.mongodb.net:27017,'
            'cluster0-shard-00-01-5pmzk.mongodb.net:27017,'
            'cluster0-shard-00-02-5pmzk.mongodb.net:27017'
            '/test?ssl=true'
            '&replicaSet=Cluster0-shard-0'
            '&authSource=admin'
            '&retryWrites=true'
        )
    )

    return client

mongodb_client = login_mongodb_cloud()
log.info(f"MongoDB client: {mongodb_client}")
