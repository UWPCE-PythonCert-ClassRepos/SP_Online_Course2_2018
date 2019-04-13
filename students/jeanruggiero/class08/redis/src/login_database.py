"""
    module that will login to neo4j
"""

import configparser
from pathlib import Path
import redis
import pymongo


config_file = Path(__file__).parent.parent / '.config/config.ini'
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
        r = redis.StrictRedis(host=host, port=port, password=pw, decode_responses=True)

    except Exception as e:
        print(f'error: {e}')

    return r

def login_mongodb_cloud():
    """
        connect to mongodb and login
    """

    try:
        config.read(config_file)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]

    except Exception as e:
        print(f'error: {e}')

    client = pymongo.MongoClient(f"mongodb://{user}:{pw}@cluster0-shard-00-00-ofcip.mongodb.net:27017,cluster0-shard-00-01-ofcip.mongodb.net:27017,cluster0-shard-00-02-ofcip.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")

    return client

