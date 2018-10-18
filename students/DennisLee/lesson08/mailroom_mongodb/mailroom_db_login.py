"""
module that will login to the MongoDb database consistently
"""

import configparser
from pathlib import Path
import pymongo

import mailroom_utilities

LOG = mailroom_utilities.configure_logger(
    'default', '../logs/login_databases_dev.log'
)
CONFIG_FILE = Path(
    __file__
).parent / '.config/config.ini'

CONFIG = configparser.ConfigParser()

def login_mongodb_cloud():
    """
    connect to mongodb and login
    """

    LOG.info('Here is where we use the connect to mongodb.')
    LOG.info('Note use of f string to embed the user & password (from the tuple).')
    try:
        CONFIG.read(CONFIG_FILE)
        user = CONFIG["mongodb_cloud"]["user"]
        pw = CONFIG["mongodb_cloud"]["pw"]

    except Exception as e:
        print(f'error: {e}')

    client = pymongo.MongoClient(
        f'mongodb://{user}:{pw}'
        '@cluster0-shard-00-00-5pmzk.mongodb.net:27017,'
        'cluster0-shard-00-01-5pmzk.mongodb.net:27017,'
        'cluster0-shard-00-02-5pmzk.mongodb.net:27017'
        '/test?ssl=true'
        '&replicaSet=Cluster0-shard-0'
        '&authSource=admin'
        '&retryWrites=true'
    )
    return client

MONGODB_CLIENT = login_mongodb_cloud()
LOG.info(f"MongoDB client: {MONGODB_CLIENT}")
