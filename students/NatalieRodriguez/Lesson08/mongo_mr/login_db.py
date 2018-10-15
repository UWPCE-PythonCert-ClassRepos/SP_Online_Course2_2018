"""
    login info for the database
"""

import configparser
from pathlib import Path
import pymongo
import utilities

log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


def login_mongodb_cloud():
    """
        connect to mongodb and login
    """

    log.info('Connecting to mongodb.')
    log.info('Note use of f string to embed the user & password (from the tuple).')
    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]

    except Exception as e:
        print(f'error: {e}')

    client = pymongo.MongoClient(f'mongodb://{user}:{pw}'
                                 '@cluster0-shard-00-00-dsill.mongodb.net:27017,'
                                 'cluster0-shard-00-01-dsill.mongodb.net:27017,'
                                 'cluster0-shard-00-02-dsill.mongodb.net:27017/test'
                                 '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true')

    return client